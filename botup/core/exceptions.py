class StateManagerException(Exception):
    pass


IsNotPrivateUpdate = StateManagerException('Update is not private')
