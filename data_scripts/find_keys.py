

def find_keys(hdrs, db):
    '''
        This function searches for keys that are stored via filestore in a
        database, and gathers the SPEC id's from them.

        For example:
            from databroker import Broker
            db = Broker.named("chx")
            hdrs = db(since="2018-01-01", until="2018-04-01")
            find_keys(hdrs, db)
    '''
    FILESTORE_KEY = "FILESTORE:"
    keys_dict = dict()
    for hdr in hdrs:
        for stream_name in hdr.stream_names:
            events = hdr.events(stream_name=stream_name)
            events = iter(events)
            while True:
                try:
                    event = next(events)
                    if "filled" in event:
                        # there are keys that may not be filled
                        for key, val in event['filled'].items():
                            if key not in keys_dict and not val:
                                # get the datum
                                if key in event['data']:
                                    datum_id = event['data'][key]
                                    resource = db.reg.resource_given_datum_id(datum_id)
                                    keys_dict[key] = resource['spec']
                except StopIteration:
                    break
                except KeyError:
                    continue
    return keys_dict

'''
Example:

from databroker import Broker
db = Broker.named("chx")
hdrs = db(start_time="2018-01-01", stop_time="2018-04-01")
# get the keys name
keys_dict = find_keys(hdrs, db)
'''
