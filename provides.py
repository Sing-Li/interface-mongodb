#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class MongoDBServer(RelationBase):
    scope = scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.
    auto_accessors = ['hostname', 'port', 'replset']

    @hook('{provides:mongodb}-relation-{joined}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        if self.connection_string():
            self.set_state('{relation_name}.database.available')

    def connection_string(self):
        """
        Get the connection string, if available, or None.
        """
        data = {
            'hostname': self.hostname(),
            'port': self.port(),
            'repel': self.replset(),
        }
        if all(data.values()):
            return str.format('{hostname}:{port}', **data)
        return None
