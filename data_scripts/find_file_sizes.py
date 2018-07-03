def file_sizes(hdrs, db):
    file_sizes = list()
    FILESTORE_KEY = "FILESTORE:"

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
                            # if this is true, then we have a datum
                            if not val:
                                # get the datum
                                if key in event['data']:
                                    datum_id = event['data'][key]
                                    resource = db.reg.resource_given_datum_id(datum_id)
                                    resource_id = resource['uid']
                                    datum_gen = db.reg.datum_gen_given_resource(resource_id)
                                    datum_kwargs = [datum['datum_kwargs'] for
                                                    datum in datum_gen]
                                    # get the file handler using this
                                    fh = db.reg.get_spec_handler(resource_id)
                                    print(fh)
                                    file_sizes = fh.get_file_sizes()
                                    print(file_sizes)
                except StopIteration:
                    break
                #except KeyError:
                    #continue
    return file_sizes

