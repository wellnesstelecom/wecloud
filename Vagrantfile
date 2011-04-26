
Vagrant::Config.run do |config|
  config.vm.box = "base" 
  config.vm.provision :shell, :path => "setup.sh"
  config.vm.forward_port("ssh", 22, 2222, :auto => true)
end

