from store.datastore_strategies import UniqueIdentifierIndexing, MultiIdentifierIndexing, ListIndexing
from store.datastore_strategies import as_int, as_string, as_boolean

class FileConfiguration():
    def __init__(self, fields, out_links, in_links, description, name):
        self.fields = fields
        self.out_links = out_links
        self.in_links = in_links
        self.description = description
        self.name = name

def get_configuration(entity):
    ''' Transforms a json description into an zenmelco Entity'''
    fields = []
    out_links  = {}
    in_links = {}
    description = ""
    name = ""
    if entity == "Organizations":
        # Field definition
        fields.append(UniqueIdentifierIndexing("_id", as_int))
        fields.append(UniqueIdentifierIndexing("url", as_string))
        fields.append(UniqueIdentifierIndexing("external_id", as_string))
        fields.append(UniqueIdentifierIndexing("name", as_string))
        fields.append(MultiIdentifierIndexing("created_at", as_int))
        fields.append(MultiIdentifierIndexing("details", as_string))
        fields.append(MultiIdentifierIndexing("shared_tickets", as_boolean))
        fields.append(ListIndexing("domain_names"))
        fields.append(ListIndexing("tags"))

        # Referenced by other files
        in_links["organization_id"] = "Tickets,Users"
        # field to be returned for short description
        description = "name"
        # name to be used for in links
        name = "organization"
    elif entity == "Tickets":
        # Field definition
        fields.append(UniqueIdentifierIndexing("_id", as_string))
        fields.append(UniqueIdentifierIndexing("url", as_string))
        fields.append(UniqueIdentifierIndexing("external_id", as_string))
        fields.append(MultiIdentifierIndexing("created_at", as_int))
        fields.append(MultiIdentifierIndexing("type", as_string))
        fields.append(MultiIdentifierIndexing("subject", as_string))
        fields.append(MultiIdentifierIndexing("description", as_string))
        fields.append(MultiIdentifierIndexing("priority", as_string))
        fields.append(MultiIdentifierIndexing("status", as_string))
        fields.append(MultiIdentifierIndexing("submitter_id", as_int))
        fields.append(MultiIdentifierIndexing("assignee_id", as_int))
        fields.append(MultiIdentifierIndexing("organization_id", as_int))
        fields.append(MultiIdentifierIndexing("has_incidents", as_boolean))
        fields.append(MultiIdentifierIndexing("due_at", as_int))
        fields.append(MultiIdentifierIndexing("via", as_string))
        fields.append(ListIndexing("tags"))

        # Reference to other files
        out_links["submitter_id"] = "Users"
        out_links["assignee_id"] = "Users"
        out_links["organization_id"] = "Organizations"
        # field to be returned for short description
        description = "subject"
        # name to be used for in links
        name = "ticket"
    elif entity == "Users":
        # Field definition
        fields.append(UniqueIdentifierIndexing("_id", as_int))
        fields.append(UniqueIdentifierIndexing("url", as_string))
        fields.append(UniqueIdentifierIndexing("external_id", as_string))
        fields.append(UniqueIdentifierIndexing("name", as_string))
        fields.append(UniqueIdentifierIndexing("phone", as_string))
        fields.append(MultiIdentifierIndexing("alias", as_string))
        fields.append(MultiIdentifierIndexing("created_at", as_int))
        fields.append(MultiIdentifierIndexing("active", as_boolean))
        fields.append(MultiIdentifierIndexing("verified", as_boolean))
        fields.append(MultiIdentifierIndexing("shared", as_boolean))
        fields.append(MultiIdentifierIndexing("locale", as_string))
        fields.append(MultiIdentifierIndexing("timezone", as_string))
        fields.append(MultiIdentifierIndexing("last_login_at", as_int))
        fields.append(MultiIdentifierIndexing("email", as_string))
        fields.append(MultiIdentifierIndexing("signature", as_string))
        fields.append(MultiIdentifierIndexing("organization_id", as_int))
        fields.append(MultiIdentifierIndexing("suspended", as_boolean))
        fields.append(MultiIdentifierIndexing("role", as_string))
        fields.append(ListIndexing("tags"))

        # Reference to other files
        out_links["organization_id"] = "Organizations"
        
        # Referenced by other files
        in_links["submitter_id"] = "Tickets"
        in_links["assignee_id"] = "Tickets"
        # field to be returned for short description
        description = "name"
        # name to be used for in links
        name = "user"
        
    return FileConfiguration(fields, out_links, in_links, description, name)