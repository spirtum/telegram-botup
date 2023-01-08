import operator
import re
from calendar import Calendar, month_name
from datetime import datetime, timedelta

from botup.navigation import Navigation
from botup.widget import Widget, Context
from botup.core.dispatcher import Dispatcher
from botup.core.types import InlineKeyboardMarkup, InlineKeyboardButton


class DatePicker(Widget):

    def __init__(self, key: str, message_text: str = 'Date picker'):
        super().__init__(key)
        self._message_text = message_text

    def build(self, dispatcher: Dispatcher):
        dispatcher.register_callback_handler('left', self._clb_month)
        dispatcher.register_callback_handler('right', self._clb_month)
        dispatcher.register_callback_handler('left_year', self._clb_year)
        dispatcher.register_callback_handler('right_year', self._clb_year)
        dispatcher.register_callback_handler('back', self._clb_back)
        dispatcher.register_command_handler('/back', self._cmd_back)
        dispatcher.register_callback_handler(re.compile('^day'), self._clb_day)

    async def entry(self, ctx: Context, *args, **kwargs):
        start_date = kwargs.get('start_date') or datetime.now()
        assert isinstance(start_date, datetime)

        await ctx.state_manager.set(
            chat_id=ctx.chat_id,
            key='date-picker',
            value=start_date.strftime('%Y-%m'),
            section='botup'
        )
        await ctx.api.send_message(
            chat_id=ctx.chat_id,
            text=self._message_text,
            reply_markup=self._calendar_keyboard(start_date.year, start_date.month)
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
        await ctx.api.answer_callback_query(ctx.update.callback_query.id)

        func = operator.sub if ctx.update.callback_query.data == 'left' else operator.add

        year_month = await ctx.state_manager.get(
            chat_id=ctx.chat_id,
            key='date-picker',
            section='botup'
        )
        date = datetime.strptime(year_month, '%Y-%m')
        new_date = func(date, timedelta(weeks=4))
        if new_date.month == date.month:
            new_date = func(new_date, timedelta(weeks=1))

        await ctx.state_manager.set(
            chat_id=ctx.chat_id,
            key='date-picker',
            value=new_date.strftime('%Y-%m'),
            section='botup'
        )

        await ctx.api.send_message(
            chat_id=ctx.chat_id,
            text=self._message_text,
            reply_markup=self._calendar_keyboard(new_date.year, new_date.month)
        )

    async def _clb_year(self, ctx: Context):
        await ctx.api.answer_callback_query(ctx.update.callback_query.id)

        func = operator.sub if ctx.update.callback_query.data == 'left_year' else operator.add
        year_month = await ctx.state_manager.get(
            chat_id=ctx.chat_id,
            key='date-picker',
            section='botup'
        )
        date = datetime.strptime(year_month, '%Y-%m')
        new_date = date.replace(year=func(date.year, 1))
        await ctx.state_manager.set(
            chat_id=ctx.chat_id,
            key='date-picker',
            value=new_date.strftime('%Y-%m'),
            section='botup'
        )

        await ctx.api.send_message(
            chat_id=ctx.chat_id,
            text=self._message_text,
            reply_markup=self._calendar_keyboard(new_date.year, new_date.month)
        )

    async def _clb_day(self, ctx: Context):
        await ctx.api.answer_callback_query(ctx.update.callback_query.id)
        _, date_str = ctx.update.callback_query.data.split()
        nav = await Navigation.of(ctx)
        await nav.pop(botup_date_picker_result=datetime.strptime(date_str, '%Y-%m-%d'))

    async def _clb_back(self, ctx: Context):
        await ctx.api.answer_callback_query(ctx.update.callback_query.id)
        nav = await Navigation.of(ctx)
        await nav.pop()

    async def _clb_none(self, ctx: Context):
        await ctx.api.answer_callback_query(ctx.update.callback_query.id)

    async def _cmd_back(self, ctx: Context):
        nav = await Navigation.of(ctx)
        await nav.pop()
