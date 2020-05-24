from requests.adapters import HTTPAdapter
from dns.resolver import Resolver

import tldextract

class SmartdnsAdapter(HTTPAdapter):
    def resolve(self, host, record_type):
        smartdns = Resolver()
        smartdns.nameservers = ['54.229.171.243', '54.93.173.153']  # SmartDNS dns address
        answers = smartdns.query(host, record_type)
        for rdata in answers:
            return str(rdata)

    def get_connection(self, url, proxies=None):
        ext = tldextract.extract(url)
        fqdn = ".".join([ext.subdomain, ext.domain, ext.suffix])

        print("FQDN: {}".format(fqdn))
        a_record = self.resolve(fqdn, 'A')
        print("A record: {}".format(a_record))

        resolved_url = url.replace(fqdn, a_record)  # NOTE: Replace first occurrence only
        print("Resolved URL: {}".format(resolved_url))

        return super().get_connection(resolved_url, proxies=proxies)


