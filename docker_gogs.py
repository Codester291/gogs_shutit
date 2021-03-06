
# Created from dockerfile: https://github.com/gogits/gogs/raw/master/docker/blocks/docker_gogs/Dockerfile
# Maintainer:              
from shutit_module import ShutItModule

class docker_gogs(ShutItModule):

	def is_installed(self, shutit):
		return False

	def build(self, shutit):
		shutit.install('build-essential ca-certificates curl bzr git mercurial unzip wget')
		#shutit.install('redis-server')
		shutit.send('export GOLANG_VERSION=1.3')
		shutit.send('curl -sSL http://golang.org/dl/go$GOLANG_VERSION.src.tar.gz | tar -v -C /usr/src -xz')
		shutit.send('pushd /usr/src/go')
		shutit.send('pushd src')
		shutit.send('./make.bash --no-clean 2>&1')
		shutit.send('export PATH=/usr/src/go/bin:$PATH')
		shutit.send('mkdir -p /go/src')
		shutit.send('export GOPATH=/go')
		shutit.send('export PATH=/go/bin:$PATH')
		shutit.send('pushd /go')
		shutit.send('useradd -m git')
		shutit.send('echo "git ALL = NOPASSWD: ALL" > /etc/sudoers.d/git')
		shutit.send('export GOGS_PATH=$GOPATH/src/github.com/gogits/gogs')
		shutit.send('export GOGS_CUSTOM_CONF_PATH=$GOGS_PATH/custom/conf')
		shutit.send('export GOGS_CUSTOM_CONF=$GOGS_CUSTOM_CONF_PATH/app.ini')
		shutit.send('go get -u -d github.com/gogits/gogs')
		shutit.send('pushd /go/src/github.com/gogits/gogs')
		shutit.send('go build github.com/gogits/gogs')
		shutit.send('chown -R git $GOGS_PATH')
		shutit.multisend('echo "CREATE DATABASE IF NOT EXISTS gogs CHARACTER SET utf8 COLLATE utf8_general_ci" | mysql -p',{'assword':shutit.cfg['shutit.tk.mysql.mysql']['root_password']})
		shutit.send('export HOME=/home/git')
		shutit.send('export USER=git')
		shutit.send('export PATH=$GOGS_PATH:$PATH')
		shutit.add_to_bashrc('export HOME=/home/git')
		shutit.add_to_bashrc('export USER=git')
		shutit.add_to_bashrc('export PATH=$GOGS_PATH:$PATH')
		shutit.send('git config --global user.name "GoGS"')
		shutit.send('popd')
		shutit.send('popd')
		shutit.send('popd')
		shutit.send('popd')
		shutit.send_file('/home/git/start_gogs.sh',"""#!/bin/bash
export USER=git
sudo /root/start_mysql.sh
cd /go/src/github.com/gogits/gogs
./gogs web
""")
		shutit.send('chmod +x /home/git/start_gogs.sh')
		shutit.send('chown git:git /home/git/start_gogs.sh')
		return True

	def start(self,shutit):
		shutit.send('/start_gogs.sh &')
		return True

	def stop(self,shutit):
		#shutit.send('''ps -ef | grep start_gogs | grep -v grep | awk '{print $1}' | xargs kill ''')
		return True

	def finalize(self, shutit):
		return True

	def test(self, shutit):
		return True

	def is_installed(self, shutit):
		return False

	def get_config(self, shutit):
		return True

def module():
		return docker_gogs(
				'gogs.io.docker_gogs.docker_gogs', 598111096.00,
				description='',
				maintainer='',
				depends=['shutit.tk.mysql.mysql']
		)
