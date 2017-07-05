# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
VBOXNAME = "alerts-dev"
VBOXRAM = 2048

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.ssh.forward_agent = true
  config.vm.box = "ubuntu/xenial64"

  #XXX vagrant-vbguest has incompatibilities with vagrant-cachier /apt/list/...
  if Vagrant.has_plugin?("vagrant-vbguest")
      config.vbguest.auto_update = true
      config.vbguest.installer = VagrantVbguest::Installers::Ubuntu
  end

  config.vm.define "virtualbox" do |virtualbox|

    virtualbox.vm.network :private_network, ip: "10.1.1.2"
    if ENV['USER'] == 'runyaga'
        virtualbox.vm.network :public_network, ip: "172.16.1.3", bridge: 'en0: Wi-Fi (AirPort)'
    else
        virtualbox.vm.network :public_network, ip: "172.16.1.3"
    end
    virtualbox.vm.network "forwarded_port", guest: 8080, host: 8080

    virtualbox.vm.provision :shell,
    :inline => "(grep -q -E '^mesg n$' /root/.profile && " \
               "sed -i 's/^mesg n$/tty -s \\&\\& mesg n/g' /root/.profile && " \
               "echo 'Ignore the previous error about stdin not being a tty. Fixing it now...') || exit 0;"

    virtualbox.vm.provision :shell, :path => "provision.sh", :args=>VBOXNAME

    config.vm.synced_folder ".", "/vagrant"
    
    if ENV['USER'] == 'frapell'
        if Vagrant.has_plugin?("vagrant-cachier")
          config.cache.scope = :box
          config.cache.enable :apt_lists
          config.cache.enable :apt
          config.cache.enable :npm
        end
    end
 end

  config.vm.provider "virtualbox" do |vb|
    if ENV['USER'] == 'frapell'
        # Intentionally left blank
    else
        vb.memory = VBOXRAM
    end
  end

  if Vagrant.has_plugin?("vagrant-triggers")
      if ENV['USER'] == 'frapell'
        # Intentionally left blank
    else
        config.trigger.after :destroy do
        # delete virtualenv leftovers
        run "rm -rf bin lib include"

        # delete buildout leftovrs
        run "rm -rf parts var eggs develop-eggs cache .mr.developer.cfg .installed.cfg local"
        end
    end
  end

end
