import yaml
import requests
import pycurl
import io
import urllib.parse
import chardet
from datetime import datetime

SETTING_FILENAME = "ddns-updater.yml"

class DDNSUpdater():

    def __init__( self ):
        self.settings = None
        self.load_settings()

    def load_settings( self ):
        f = open( SETTING_FILENAME, "r" )
        self.settings = yaml.load( f )
        f.close()

    def save_settings( self ):
        f = open( SETTING_FILENAME, "w" )
        f.write( yaml.dump( self.settings ) )
        f.close()

    def put_log( self, line ):
        print( datetime.now().strftime( "%Y/%m/%d %H:%M:%S" ) + ": " + line )

    def get_http_resp( self, url ):
        buffer = io.BytesIO()
        curl = pycurl.Curl()
        curl.setopt( pycurl.URL, url )
        curl.setopt( pycurl.WRITEFUNCTION, buffer.write )
        curl.perform()
        charcode = chardet.detect( buffer.getvalue() )[ 'encoding' ]
        return ( curl.getinfo( pycurl.HTTP_CODE ), buffer.getvalue().decode( charcode ).rstrip( '\n' ) )

    def get_current_ipaddr( self ):
        ipaddr = None
        status_code, text = self.get_http_resp( self.settings[ 'ipcheck_url'] )
        if status_code == requests.codes.ok:
            ipaddr = text
        else:
            raise Exception
        return ipaddr

    def run( self ):
        ipaddr = self.get_current_ipaddr()
        for setting in self.settings[ 'update_list' ]:
            if ipaddr != setting[ 'current_ip' ]:
                if self.update_ddns( setting ):
                    previous_ip = setting[ 'current_ip' ]
                    setting[ 'current_ip' ] = ipaddr
                    self.save_settings()
                    self.put_log( setting[ 'name' ] + " > IP address is updated: " + ipaddr )

    def is_need_to_update( self, setting ):
        return self.current_ip == setting[ 'current_ip' ]

    def update_ddns( self, setting ):
        status_code, text = self.get_http_resp( setting[ 'uri' ] + "?" + urllib.parse.urlencode( setting[ 'params' ] ) )
        return status_code == requests.codes.ok

if __name__ == "__main__":
    updater = DDNSUpdater()
    updater.run()
