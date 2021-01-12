from botup.dispatcher import DictStateManager, StateDispatcher, Dispatcher

from tests import utils


def test_reverse_dispatching():
    update = utils.command_update_by_text('/test')
    start_update = utils.command_update_by_text('/start')

    sm = DictStateManager()
    dispatcher = StateDispatcher(sm, 'main')
    child_one = Dispatcher()
    child_two = Dispatcher()

    dispatcher.register_state('1', child_one)
    dispatcher.register_state('2', child_two)

    dispatcher_calls, dispatcher_updates = list(), list()
    child_one_calls, child_one_updates = list(), list()
    child_two_calls, child_two_updates = list(), list()

    @dispatcher.command_handler('test')
    def dispatcher_test(c, u):
        dispatcher_calls.append(dispatcher_test)
        dispatcher_updates.append(u)

    @dispatcher.command_handler('start')
    def dispatcher_start(c, u):
        dispatcher_calls.append(dispatcher_start)
        dispatcher_updates.append(u)

    @child_one.command_handler('test')
    def child_one_test(c, u):
        child_one_calls.append(child_one_test)
        child_one_updates.append(u)

    @child_two.command_handler('test')
    def child_two_test(c, u):
        child_two_calls.append(child_two_test)
        child_two_updates.append(u)

    dispatcher.handle(update)
    assert dispatcher_calls[-1] == dispatcher_test
    assert len(dispatcher_updates) == 1
    assert len(child_one_updates) == 0
    assert len(child_two_updates) == 0

    sm.update = update
    sm.set('main', '1')

    dispatcher.handle(update)
    assert child_one_calls[-1] == child_one_test
    assert len(dispatcher_updates) == 1
    assert len(child_one_updates) == 1
    assert len(child_two_updates) == 0

    sm.update = update
    sm.set('main', '2')

    dispatcher.handle(update)
    assert child_two_calls[-1] == child_two_test
    assert len(dispatcher_updates) == 1
    assert len(child_one_updates) == 1
    assert len(child_two_updates) == 1

    dispatcher.handle(start_update)
    assert dispatcher_calls[-1] == dispatcher_start
    assert dispatcher_updates[-1] == start_update
    assert len(dispatcher_updates) == 2
    assert len(child_one_updates) == 1
    assert len(child_two_updates) == 1


def test_direct_handling_decorator():
    update = utils.command_update_by_text('/test')

    sm = DictStateManager()
    dispatcher = StateDispatcher(sm, 'main')
    child_one = Dispatcher()
    dispatcher.register_state('1', child_one)
    dispatcher_updates = list()

    @dispatcher.command_handler('test')
    def dispatcher_test(c, u):
        dispatcher_updates.append(u)

    dispatcher.handle(update)
    assert len(dispatcher_updates) == 1

    sm.update = update
    sm.set('main', '1')

    dispatcher.handle(update)
    assert len(dispatcher_updates) == 2

    # with direct handling

    @dispatcher.command_handler('test')
    @dispatcher.direct_handling
    def dispatcher_test_direct_handling(c, u):
        dispatcher_updates.append(u)

    sm.update = update
    assert sm.get('main') == '1'

    dispatcher.handle(update)
    assert len(dispatcher_updates) == 2

    sm.update = update
    sm.reset('main')
    assert not sm.get('main')
    dispatcher.handle(update)
    assert len(dispatcher_updates) == 3
