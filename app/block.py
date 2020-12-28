import base64


class Block:

    def __init__(self, block_result):
        self.data = block_result['result']

    def to_dict(self):
        out = {'height':self.__get_height(),
               'txs':self.__parse_tx_timeseries_points(),
               'events':self.__get_events()}
        return out
  
    def __get_txs(self):
        txs = self.data['txs_results']
        if txs:
            return [self.__parse_tx(i) for i in txs]
        else:
            return None

    def __get_events(self):
        events = [self.__parse_event_dict(i) for i in self.data['begin_block_events']]
        return events
  
    def __parse_tx(self, tx):
        out = {"events":self.__parse_events(tx['events'])}
        out['gas_wanted'], out['gas_used'] = self.__get_gas(tx)
        return out

    def __get_height(self):
        return int(self.data['height'])
    
    def __get_gas(self, tx):
        wanted = int(tx['gasWanted'])
        used = int(tx['gasUsed'])
        return (wanted, used)
  
    def __decode_attribute_dict(self, attr_dict):
        out = {}
        for i in attr_dict.keys():
            if attr_dict[i] != None:
                out[i] = str(base64.b64decode(attr_dict[i]), 'utf-8')
            else:
                out[i] = ''
        return out
    
    def __decode_attributes(self, attrs):
        return [self.__decode_attribute_dict(i) for i in attrs]
  
    def __parse_event_dict(self, event_dict):
        out = {'type': event_dict['type'],
               'attrs': self.__decode_attributes(event_dict['attributes'])}
        return out
  
    def __parse_events(self, events):
        return [self.__parse_event_dict(i) for i in events]

    def __parse_tx_event(self, event):
        out = []
        for i in event:
            out.append((i['key'], i['value']))
        return out

    def __parse_tx_events(self, events):
        out = []
        for i in events:
            attrs = i['attrs']
            out.extend(self.__parse_tx_event(attrs))
        return out
    
    def __parse_tx_timeseries_tx(self, tx):
        out = []
        events = tx['events']
        if events:
            out.append(('success', True))
            out.extend(self.__parse_tx_events(events))
        else:
            out.append(('success', False))
            out.append(('module', 'tx_fail'))
        out.append(('gas_wanted', tx['gas_wanted']))
        out.append(('gas_used', tx['gas_used']))
        return out
    
    def __parse_tx_timeseries_points(self):
        out = []
        height = self.__get_height()
        txs = self.__get_txs()
        if txs:
            for i in txs:
                tx = self.__parse_tx_timeseries_tx(i)
                tx.append(('height', height))
                out.append(dict(tx))
            return out
        else:
            return None

    