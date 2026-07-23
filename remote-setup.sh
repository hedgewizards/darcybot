#!/bin/bash

# Script: remote-setup.sh
# Description: Sets up a remote server using the provided IP address and SSH key.
# Usage: remote-setup.sh <server-ip> <ssh-key-path>

# Function to display usage information
usage() {
    echo "Usage: $0 <server-ip> <ssh-key-path>"
    echo "  <server-ip>      The IP address of the remote server."
    echo "  <ssh-key-path>   The path to the SSH private key file."
    echo ""
    echo "Options:"
    echo "  -h, --help       Show this help message and exit."
    exit 1
}

# Default values for arguments
server_ip=""
ssh_key_path=""

# Parse command-line options
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -h|--help)
            usage
            ;;
        -*)
            echo "Error: Unknown option '$1'"
            usage
            ;;
        *)
            if [[ -z "$server_ip" ]]; then
                server_ip="$1"
            elif [[ -z "$ssh_key_path" ]]; then
                ssh_key_path="$1"
            else
                echo "Error: Unexpected argument '$1'"
                usage
            fi
            ;;
    esac
    shift
done

# Check if required arguments are provided
if [[ -z "$server_ip" || -z "$ssh_key_path" ]]; then
    echo "Error: Missing required arguments."
    usage
fi

# Validate the arguments
if [[ ! "$server_ip" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Invalid server IP address."
    usage
fi

if [[ ! -f "$ssh_key_path" ]]; then
    echo "Error: SSH key file not found at '$ssh_key_path'."
    usage
fi
# Remove the old host key from known_hosts
ssh-keygen -R "$server_ip"

# Create /root/scripts directory on the server
ssh -i "$ssh_key_path" root@"$server_ip" "mkdir -p /root/scripts"

# Copy local scripts to the server's /root/scripts directory
scp -i "$ssh_key_path" scripts/remote/* root@"$server_ip":/root/scripts/

# Run /root/scripts/local-setup.sh on the server
ssh -i "$ssh_key_path" root@"$server_ip" "chmod +x /root/scripts/local-setup.sh"
ssh -i "$ssh_key_path" root@"$server_ip" "/root/scripts/local-setup.sh"

# Create /root/src/tropical-server/cfg directory on the server
ssh -i "$ssh_key_path" root@"$server_ip" "mkdir -p /root/src/tropical-server/cfg"

# Copy setsteamaccount.cfg to the server's /root/src/tropical-server/cfg directory
scp -i "$ssh_key_path" cfg/setsteamaccount.cfg root@"$server_ip":/root/src/tropical-server/cfg/

# Run /root/src/update.sh on the server
ssh -i "$ssh_key_path" root@"$server_ip" "chmod +x /root/scripts/update.sh"
ssh -i "$ssh_key_path" root@"$server_ip" "/root/scripts/update.sh --skip-pull"
