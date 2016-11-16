#!/usr/bin/env python3

from charms.reactive import (
    hook,
    RelationBase,
    scopes,
)


class MongoDBPeer(RelationBase):
    # The peer class uses the unit scope to communicate with individual units
    scope = scopes.UNIT

    @hook('{peers:mongodb}-relation-{joined,departed,broken}')
    def something(self):
        '''When peers join set the create certificate signing request state.'''
        # Get the conversation scoped to the unit name.
        conv = self.conversation()
        # Set the start state here for the layers to handle the logic.
        conv.set_state('{relation_name}.new-peers')

    def peers(self):
        '''Return an iterator of (unit-name, address)'''
        convos = self.conversations()

        for conv in convos:
            yield (conv.scope.replace('/', '-'),
                   conv.get_remote('private-address'))
