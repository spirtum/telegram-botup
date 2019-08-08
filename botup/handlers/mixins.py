class PatternMixin:

    def get_handler(self, command):
        handler = self.handlers.get(command) if command != '*' else None
        if not handler:
            for pattern in (c for c in self.handlers.keys() if c.endswith('*')):
                if pattern[:-1] in command:
                    handler = self.handlers[pattern]
                    break
        return handler
