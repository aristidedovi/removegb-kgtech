#!/bin/bash

# Check if Docker is already installed
if command -v docker &> /dev/null
then
    echo "Docker is already installed, skipping Docker installation."
else
    # Update package lists and upgrade the system
    sudo apt update && sudo apt upgrade -y

    # Install dependencies
    sudo apt-get install -y curl apt-transport-https ca-certificates software-properties-common

    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    # Add Docker's official APT repository
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

    # Update the package list to include Docker's repo
    sudo apt update

    # Install Docker CE (Community Edition)
    sudo apt install -y docker-ce

    echo "Docker has been installed."
fi

# Check if Docker Compose is already installed
if command -v docker-compose &> /dev/null
then
    echo "Docker Compose is already installed, skipping Docker Compose installation."
else

    # Install Docker Compose
    curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

    # Make Docker Compose executable
    sudo chmod +x /usr/local/bin/docker-compose

    echo "Docker Compose has been installed."
fi

# Verify installations
docker --version
docker-compose --version

# Up application with docker commande
docker-compose up -d
