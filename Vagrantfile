# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ARTACK/debian-jessie"
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y python3-pip python3-dev virtualenv virtualenvwrapper nginx postgresql postgresql-contrib libpq-dev pandoc libjpeg-dev
    sudo sed -e 's/peer/trust/g' /etc/postgresql/9.4/main/pg_hba.conf | sudo tee /etc/postgresql/9.4/main/pg_hba.conf.tmp > /dev/null
    sudo mv /etc/postgresql/9.4/main/pg_hba.conf.tmp /etc/postgresql/9.4/main/pg_hba.conf
    sudo sed -e 's/md5/trust/g' /etc/postgresql/9.4/main/pg_hba.conf | sudo tee /etc/postgresql/9.4/main/pg_hba.conf.tmp > /dev/null
    sudo mv /etc/postgresql/9.4/main/pg_hba.conf.tmp /etc/postgresql/9.4/main/pg_hba.conf
    sudo systemctl restart postgresql
    sudo systemctl enable postgresql
    createuser -w -U postgres harnas
    createdb -U postgres -O harnas harnas

    sudo su - vagrant -c "mkdir /home/vagrant/.virtualenvs"
    echo "export WORKON_HOME=/home/vagrant/.virtualenvs" >> /home/vagrant/.bashrc
    echo "source /usr/share/virtualenvwrapper/virtualenvwrapper.sh" >> /home/vagrant/.bashrc

    sudo su - vagrant -c "mkdir -p /harnas/task"
  SHELL
end
