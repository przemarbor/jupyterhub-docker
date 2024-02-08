Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"
  config.vm.network "public_network"
  config.vm.synced_folder ".", "/vagrant/"
  config.vm.network "private_network", type: "dhcp"

  config.vm.provision :docker
  config.vm.provision :docker_compose, yml: "/vagrant/docker-compose.yml", rebuild: true, run: "always"
end
