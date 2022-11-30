variable "source_ami" {
  type    = string
  default = "ami-08c40ec9ead489470" 
}

variable "ssh_username" {
  type    = string  
  default = "ubuntu"
}

variable "subnet_id" {
  type    = string
  default = "subnet-07821efa79f9f961e"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}


variable "ami_user"{
  type    = string
  default = "620068443483"
}
# https://www.packer.io/plugins/builders/amazon/ebs
source "amazon-ebs" "my-ami" {
  region     = "${var.aws_region}"
  ami_name        = "csye6225_${formatdate("YYYY_MM_DD_hh_mm_ss", timestamp())}"
  ami_description = "AMI for CSYE 6225"
  ami_regions = [
    "us-east-1",
  ]
  ami_users= ["${var.ami_user}"]

  aws_polling {
    delay_seconds = 30
    max_attempts  = 50
  }


  instance_type = "t2.micro"
  source_ami    = "${var.source_ami}"
  ssh_username  = "${var.ssh_username}"
  subnet_id     = "${var.subnet_id}"

  launch_block_device_mappings {
    delete_on_termination = true
    device_name           = "/dev/sda1"
    volume_size           = 8
    volume_type           = "gp2"
  }
}

build {
  sources = ["source.amazon-ebs.my-ami"]
   
  provisioner "file" {
    source      = "gunicorn.service"
    destination ="/tmp/gunicorn.service"
   }
    provisioner "file" {
    source      = "network_file"
    destination ="/tmp/network_file"
   }
  provisioner "file" {
    source      = "webapp.zip"
    destination = "/home/ubuntu/webapp.zip"
  }
  
  provisioner "shell" {
    script ="script.sh"
 }

  post-processor "manifest" {
    output = "manifest.json"
    strip_path = true
 }
}
