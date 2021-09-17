eval `ssh-agent -s`
echo $SSH_AUTH_SOCK
echo $SSH_AGENT_PID

ssh-add ~/.ssh/github_rsa
ansible-galaxy install -r requierements.yml -vvv -p roles
kill $SSH_AGENT_PID
