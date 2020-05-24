from requests.adapters import HTTPAdapter
from urlparse import urlparse
from dns.resolver import Resolver

class SmartdnsAdapter(HTTPAdapter):
    def resolve(self, hostname):
        resolver = Resolver()
        resolver.nameservers = ['54.229.171.243', '54.93.173.153']  # SmartDNS dns addres
        answer = resolver.query(hostname, 'A')
        return answer.rrset.items[0].address

    def send(self, request, **kwargs):
        connection_pool_kwargs = self.poolmanager.connection_pool_kw

        result = urlparse(request.url)
        resolved_ip = self.resolve(result.hostname)

        request.url = request.url.replace(result.netloc, resolved_ip)

        connection_pool_kwargs['server_hostname'] = result.netloc  # SNI
        connection_pool_kwargs['assert_hostname'] = result.netloc

        # overwrite the host header
        request.headers['Host'] = result.netloc

        return super(SmartdnsAdapter, self).send(request, **kwargs)

