#!/usr/bin/env python3


from ctf_gameserver import checkerlib
import logging
import paramiko
import http.client
import socket

PORT_WEB = 9009
PORT_WEBAPP = 9008

def ssh_connect():
    def decorator(func):
        def wrapper(*args, **kwargs):
            # SSH connection setup
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            rsa_key = paramiko.RSAKey.from_private_key_file(f'/keys/team{args[0].team}-sshkey')
            client.connect(args[0].ip, username = 'root', pkey=rsa_key)

            # Call the decorated function with the client parameter
            args[0].client = client
            result = func(*args, **kwargs)

            # SSH connection cleanup
            client.close()
            return result
        return wrapper
    return decorator

class MyChecker(checkerlib.BaseChecker):
    def __init__(self, ip, team):
        checkerlib.BaseChecker.__init__(self, ip, team)
        self._baseurl = f'http://[{self.ip}]:{PORT_WEB}'
        logging.info(f"URL: {self._baseurl}")

    @ssh_connect()
    def place_flag(self, tick):
        flag = checkerlib.get_flag(tick)
        creds = self._add_new_flag(self.client, flag)
        if not creds:
            return checkerlib.CheckResult.FAULTY
        logging.info('created')
        checkerlib.store_state(str(tick), creds)
        checkerlib.set_flagid(str(tick))
        return checkerlib.CheckResult.OK
    
    def check_service(self):
        result = checkerlib.CheckResult.OK
        # check if ports are open
        if not self._check_port(self.ip, PORT_WEB) or not self._check_port(self.ip, PORT_WEBAPP):
            result = checkerlib.CheckResult.DOWN
        # check if server nginx 1.27.2
        if not self._check_nginx_version():
            result =  checkerlib.CheckResult.FAULTY
        if not self._check_functionality_is_running():
            result = checkerlib.CheckResult.FAULTY
        return result
    
    def check_flag(self, tick):
        if not self.check_service():
            return checkerlib.CheckResult.DOWN
        flag = checkerlib.get_flag(tick)
        flag_present = self._check_flag_present(flag)
        if not flag_present:
            return checkerlib.CheckResult.FLAG_NOT_FOUND
        return checkerlib.CheckResult.OK
    

     # Private Funcs - Return False if error
    def _add_new_flag(self, ssh_session, flag):
        # Execute the file creation command in the container
        command = f"docker exec injection_webapp sh -c 'echo {flag} >> /tmp/flag.txt'"
        stdin, stdout, stderr = ssh_session.exec_command(command)

        # Check if the command executed successfully
        if stderr.channel.recv_exit_status() != 0:
            return False
        
        # Return the result
        return {'flag': flag}

    def _check_port(self, ip, port):
            try:
                conn = http.client.HTTPConnection(ip, port, timeout=5)
                conn.request("GET", "/")
                response = conn.getresponse()
                return response.status == 200
            except (http.client.HTTPException, socket.error) as e:
                print(f"Exception: {e}")
                return False
            finally:
                if conn:
                    conn.close()

    @ssh_connect()
    def _check_nginx_version(self):
        ssh_session = self.client
        command = f"docker exec injection_web sh -c 'nginx -v | grep nginx/1.27.2'"
        stdin, stdout, stderr = ssh_session.exec_command(command)

        if stdout:
            return True
        else:
            return False
        
    @ssh_connect()
    def _check_flag_present(self, flag):
        ssh_session = self.client
        command = f"docker exec injection_webapp sh -c 'grep {flag} /tmp/flag.txt'"
        stdin, stdout, stderr = ssh_session.exec_command(command)
        if stderr.channel.recv_exit_status() != 0:
            return False
        output = stdout.read().decode().strip()
        return flag == output
    
    def _check_functionality_is_running(self):
        login_form = """<form action="?" method="POST" onsubmit="login();return false;">"""        login_url = "/login"
        try:
                conn = http.client.HTTPConnection(ip, port, timeout=5)
                conn.request("GET", "/")
                response = conn.getresponse()
                if response.status != 200:
                     return False
                data = response.read().lower().decode()
                if data.find(login_form.lower()) == -1:
                     #Login form not found in response html
                     return False

        except (http.client.HTTPException, socket.error) as e:
                print(f"Exception: {e}")
                return False
        finally:
                if conn:
                    conn.close()
        return True