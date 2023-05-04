from django.db import models

# Create your models here.
class ResourceType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return f'ResourceType({self.name})'

PROXY_TYPE_OPTION = (
        ('None', 'None'),
        ('HTTP', 'HTTP'),
        ('HTTPS', 'HTTPS'),
        ('SOCKS4', 'SOCKS4'),
        ('SOCKS5', 'SOCKS5'),
    )

class ProxyServer(models.Model):
    addr = models.CharField("IP address", max_length=12)
    port = models.CharField("Port", max_length=4)
    proxy_type = models.CharField("Proxy types", choices=PROXY_TYPE_OPTION, max_length=10, default='HTTP')
    def __str__(self):
        return f'ProxyServer({self.addr}, {self.port}, {self.proxy_type})'

class Resources(models.Model):
    type = models.ForeignKey("ResourceType", on_delete=models.PROTECT, help_text="select a resource type")
    name = models.CharField("Resource name", max_length=100, unique=True, help_text="the name has to be unique")
    addr = models.CharField("IP address", max_length=12, help_text="e.g. 0.0.0.0")
    port = models.CharField("Port", max_length=4)
    user_id = models.CharField("User ID", max_length=100, help_text="user id to access")
    password = models.CharField("Password", max_length=200)
    connect_addr_list = models.CharField("IP list of require connection", max_length=300, help_text="e.g. 0.0.0.0/1.1.1.1/2.2.2.2", blank=True)
    ci_agent_path = models.CharField("Path of CI agent", max_length=300, help_text="if you use this resource with CI agent such as bamboo", blank=True)
    proxy_server = models.ForeignKey("ProxyServer", on_delete=models.PROTECT, blank=True, null=True, default="None", help_text="select proxy server if necessary")
    disabled = models.BooleanField("Disabled", help_text="if the resource is not necessary")
    def __str__(self):
        return f'Resources({self.type}, {self.name}, {self.addr}, {self.port}, {self.user_id}, {self.password}, {self.connect_addr_list}, {self.proxy_server}, {self.disabled})'
