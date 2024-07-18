provider "paperspace" {
  region = "East Coast (NY2)"
  api_key = var.api_key // modify this to use your actual api key
}

data "paperspace_template" "cpu" {
  id = "tkni3aa4" // this is one of the Ubuntu Server 20.04 templates with 537MB RAM
}

data "paperspace_user" "my-user-1" {
  email = "jnm.ronquillo@gmail.com" // change to the email address of a user on your paperspace team
  team_id = "t7ysm6amj3" // modify this to use your team id 
}

resource "paperspace_script" "ssh_public_key" {
  name = "Add public ssh key"
  description = "a short description"
  script_text = <<EOF
#!/bin/bash
echo "Hello, World" >> /home/paperspace/.ssh/authorized_keys
EOF
  is_enabled = true
  run_once = true
}

resource "paperspace_script" "my-script-1" {
  name = "My Script"
  description = "a short description"
  script_text = <<EOF
#!/bin/bash
echo "Hello, World" > index.html
ufw allow 8080
nohup busybox httpd -f -p 8080 &
EOF
  is_enabled = true
  run_once = false
}

resource "paperspace_machine" "my-machine-1" {
  region = "East Coast (NY2)" // optional, defaults to provider region if not specified
  name = "Terraform Test"
  machine_type = "C1"
  size = 50
  billing_type = "hourly"
  assign_public_ip = true // optional, remove if you don't want a public ip assigned
  template_id = data.paperspace_template.cpu.id
  user_id = data.paperspace_user.my-user-1.id  // optional, remove to default
  team_id = data.paperspace_user.my-user-1.team_id
  script_id = paperspace_script.my-script-1.id // optional, remove for no script
  shutdown_timeout_in_hours = 42
  # live_forever = true # enable this to make the machine have no shutdown timeout
}

#resource "paperspace_network" "network" {
#  team_id = 00000 // change to your team's actual database id (unlike team_id everywhere else, which is your team handle)
#}