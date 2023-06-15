import operator
import re
from calendar import Calendar, month_name
from datetime import datetime, timedelta
from asyncio import gather

from botup.navigation import Navigation
from botup.widget import Widget, Context
from botup.dispatcher import Dispatcher
from botup.types import InlineKeyboardMarkup, InlineKeyboardButton


class DatePicker(Widget):

    def __init__(
            self,
            key: str,
            result_key: str = 'botup_date_picker_result',
            message_text: str = 'Date picker'
    ):
        super().__init__(key)
        self._message_text = message_text
        self._storage_section = 'botup_date_picker'
        self._storage_value_key = 'value'
        self._storage_message_id_key = 'message_id'
        self._result_key = result_key

    def build(self, dispatcher: Dispatcher):
        dispatcher.register_callback_handler('left', self._clb_month)
        dispatcher.register_callback_handler('right', self._clb_month)
        dispatcher.register_callback_handler('left_year', self._clb_year)
        dispatcher.register_callback_handler('right_year', self._clb_year)
        dispatcher.register_callback_handler('none', self._clb_none)
        dispatcher.register_callback_handler('back', self._clb_back)
        dispatcher.register_command_handler('/back', self._cmd_back)
        dispatcher.register_callback_handler(re.compile('^day'), self._clb_day)

    async def entry(self, ctx: Context, *args, **kwargs):
        start_date = kwargs.get('start_date') or datetime.now()
        message_id = kwargs.get('message_id')
        assert isinstance(start_date, datetime)

        if not message_id:
            message = await ctx.api.send_message(
                chat_id=ctx.chat_id,
                text=self._message_text,
                reply_markup=self._calendar_keyboard(start_date.year, start_date.month)
            )

            await gather(
                ctx.state_manager.set(
                    chat_id=ctx.chat_id,
                    key=self._storage_value_key,
                    value=start_date.strftime('%Y-%m'),
                    section=self._storage_section
                ),
                ctx.state_manager.set(
                    chat_id=ctx.chat_id,
                    key=self._storage_message_id_key,
                    value=str(message.message_id),
                    section=self._storage_section
                )
            )
            return

        assert isinstance(message_id, int)

        await gather(
            ctx.api.edit_message_text(
                text=self._message_text,
                chat_id=ctx.chat_id,
                message_id=message_id,
                reply_markup=self._calendar_keyboard(start_date.year, start_date.month)
            ),
            ctx.state_manager.set(
                chat_id=ctx.chat_id,
                key=self._storage_message_id_key,
                value=str(message_id),
                section=self._storage_section
            ),
            ctx.state_manager.set(
                chat_id=ctx.chat_id,
                key=self._storage_value_key,
                value=start_date.strftime('%Y-%m'),
                section=self._storage_section
            )
        )

    @staticmethod
    def _chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i+n]

    def _calendar_keyboard(self, year: int, month: int) -> InlineKeyboardMarkup:
        c = Calendar()
        lines = []

        for line in self._chunks(list(c.itermonthdates(year, month)), 7):
            args = list()

            for d in line:
                cb = InlineKeyboardButton(text='.', callback_data='none')
                if d.month == month:
                    cb = InlineKeyboardButton(text=f'{d.day}', callback_data=f"day {d.strftime('%Y-%m-%d')}")
                args.append(cb)

            lines.append(args)

        lines.append([
            InlineKeyboardButton(text='<', callback_data='left'),
            InlineKeyboardButton(text=month_name[month], callback_data='none'),
            InlineKeyboardButton(text='>', callback_data='right')
        ])
        lines.append([
            InlineKeyboardButton(text='<', callback_data='left_year'),
            InlineKeyboardButton(text=str(year), callback_data='none'),
            InlineKeyboardButton(text='>', callback_data='right_year')
        ])
        lines.append([InlineKeyboardButton(text='Back', callback_data='back')])

        return InlineKeyboardMarkup(lines)

    async def _clb_month(self, ctx: Context):
        func = operator.sub if ctx.update.callback_query.data == 'left' else operator.add

        _, message_id, year_month = await gather(
            ctx.api.answer_callback_query(ctx.update.callback_query.id),
            ctx.state_manager.get(
                chat_id=ctx.chat_id,
                section=self._storage_section,
                key=self._storage_message_id_key
            ),
            ctx.state_manager.get(
                chat_id=ctx.chat_id,
                key=self._storage_value_key,
                section=self._storage_section
            )
        )

        date = datetime.strptime(year_month, '%Y-%m')
        new_date = func(date, timedelta(weeks=4))
        if new_date.month == date.month:
            new_date = func(new_date, timedelta(weeks=1))

        await gather(
            ctx.state_manager.set(
                chat_id=ctx.chat_id,
                key=self._storage_value_key,
                value=new_date.strftime('%Y-%m'),
                section=self._storage_section
            ),
            ctx.api.edit_message_reply_markup(
                chat_id=ctx.chat_id,
                message_id=int(message_id),
                reply_markup=self._calendar_keyboard(new_date.year, new_date.month)
            )
        )

    async def _clb_year(self, ctx: Context):
        func = operator.sub if ctx.update.callback_query.data == 'left_year' else operator.add

        _, message_id, year_month = await gather(
            ctx.api.answer_callback_query(ctx.update.callback_query.id),
            ctx.state_manager.get(
                chat_id=ctx.chat_id,
                section=self._storage_section,
                key=self._storage_message_id_key
            ),
            ctx.state_manager.get(
                chat_id=ctx.chat_id,
                key=self._storage_value_key,
                section=self._storage_section
            )
        )

        date = datetime.strptime(year_month, '%Y-%m')
        new_date = date.replace(year=func(date.year, 1))

        await gather(
            ctx.state_manager.set(
                chat_id=ctx.chat_id,
                key=self._storage_value_key,
                value=new_date.strftime('%Y-%m'),
                section=self._storage_section
            ),
            ctx.api.edit_message_reply_markup(
                chat_id=ctx.chat_id,
                message_id=int(message_id),
                reply_markup=self._calendar_keyboard(new_date.year, new_date.month)
            )
        )

    async def _clb_day(self, ctx: Context):
        _, nav, message_id = await gather(
            ctx.api.answer_callback_query(ctx.update.callback_query.id),
            Navigation.of(ctx),
            ctx.state_manager.get(
                chat_id=ctx.chat_id,
                section=self._storage_section,
                key=self._storage_message_id_key
            )
        )
        _, date_str = ctx.update.callback_query.data.split()
        await gather(
            ctx.api.delete_message(
                chat_id=ctx.chat_id,
                message_id=message_id
            ),
            nav.pop(**{self._result_key: datetime.strptime(date_str, '%Y-%m-%d')})
        )

    async def _clb_back(self, ctx: Context):
        _, nav, message_id = await gather(
            ctx.api.answer_callback_query(ctx.update.callback_query.id),
            Navigation.of(ctx),
            ctx.state_manager.get(
                chat_id=ctx.chat_id,
                section=self._storage_section,
                key=self._storage_message_id_key
            )
        )
        await gather(
            ctx.api.delete_message(
                chat_id=ctx.chat_id,
                message_id=message_id
            ),
            nav.pop()
        )

    async def _clb_none(self, ctx: Context):
        await ctx.api.answer_callback_query(ctx.update.callback_query.id)

    async def _cmd_back(self, ctx: Context):
        nav, message_id = await gather(
            Navigation.of(ctx),
            ctx.state_manager.get(
                chat_id=ctx.chat_id,
                section=self._storage_section,
                key=self._storage_message_id_key
            )
        )
        await gather(
            ctx.api.delete_message(
                chat_id=ctx.chat_id,
                message_id=message_id
            ),
            nav.pop()
        )
