from contextlib import contextmanager


@contextmanager
def disconnect_signal(signal, receiver, sender, dispatch_uid=None, weak=True):
    signal.disconnect(
        receiver=receiver,
        sender=sender,
        dispatch_uid=dispatch_uid,
    )
    yield
    signal.connect(
        receiver=receiver,
        sender=sender,
        dispatch_uid=dispatch_uid,
        weak=weak
    )
