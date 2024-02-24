# Kubernetes Cluster Setup

This README provides an explanation of the steps involved in setting up a Kubernetes cluster on a Linux system using the provided script. Before proceeding, make sure you have administrative privileges on the system.

## Step 1: Disable Swap

```shell
sudo swapoff -
sudo sed -i '/ swap / s/^/#/' /etc/fstab
```aCertainly, let's dive into more detail for each step in the provided Kubernetes setup script:

### Step 1: Disable Swap
```shell
sudo swapoff -
sudo sed -i '/ swap / s/^/#/' /etc/fstab
```
- `sudo swapoff -`: Disables the swap space immediately, which is recommended for Kubernetes because swap can lead to performance issues.
- `sudo sed -i '/ swap / s/^/#/' /etc/fstab`: Uses `sed` to comment out any lines in the `/etc/fstab` file that reference swap partitions. This ensures that swap won't be automatically activated upon system reboot.

### Step 2: Load Kernel Modules
```shell
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
    overlay
    br_netfilter
EOF
sudo modprobe overlay
sudo modprobe br_netfilter
```
- This part creates a configuration file `/etc/modules-load.d/k8s.conf` with the necessary kernel modules for Kubernetes:
  - `overlay`: A filesystem driver used for container storage.
  - `br_netfilter`: A bridge network filter required for Kubernetes networking.
- `sudo modprobe overlay` and `sudo modprobe br_netfilter` load these kernel modules immediately to make them available.

### Step 3: Configure sysctl Parameters
```shell
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
    net.bridge.bridge-nf-call-iptables  = 1
    net.bridge.bridge-nf-call-ip6tables = 1
    net.ipv4.ip_forward                 = 1
EOF
sudo sysctl --system
```
- This step involves configuring kernel parameters using the `sysctl` utility, which is needed for Kubernetes networking and IP forwarding.
- The parameters being set:
  - `net.bridge.bridge-nf-call-iptables` and `net.bridge.bridge-nf-call-ip6tables`: These enable iptables to correctly handle bridged traffic in Kubernetes.
  - `net.ipv4.ip_forward`: This enables IP forwarding, allowing packets to flow through the system.

### Step 4: Set Up Package Management
```shell
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl
```
- This part updates the package list using `apt-get update` and installs several essential packages required for setting up repositories and downloading files securely.
  - `apt-transport-https`: Enables the use of HTTPS transport for package management.
  - `ca-certificates`: Ensures that the system has the necessary CA certificates for secure communication.
  - `curl`: Used for making HTTP requests, which is handy for downloading files.

### Step 5: Add Kubernetes Repository
```shell
sudo mkdir /etc/apt/keyrings
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-archive-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
```
- This section manages the addition of the Kubernetes repository to your system's package sources:
  - It starts by creating a directory for APT keyrings in `/etc/apt/keyrings`.
  - It then fetches the GPG key for the Kubernetes repository and stores it as a binary file.
  - Next, it appends an APT source entry to `/etc/apt/sources.list.d/kubernetes.list`, ensuring that the Kubernetes repository is properly recognized.
  - Finally, it updates the package list again, now including the Kubernetes repository.

### Step 6: Install Kubernetes and Docker
```shell
sudo apt install -y kubelet kubeadm kubectl
sudo apt install -y docker.io
```
- This part installs the main Kubernetes components and Docker:
  - `kubelet`, `kubeadm`, and `kubectl` are core Kubernetes tools.
  - `docker.io` is the Docker container runtime required for running containers in the Kubernetes cluster.

### Step 7: Configure Containerd
```shell
mkdir -p /etc/containerd
sudo sed -i 's/ SystemdCgroup = false/ SystemdCgroup = true/' /etc/containerd/config.toml
sudo sh -c "containerd config default > /etc/containerd/config.toml"
sudo sed -i 's/ SystemdCgroup = false/ SystemdCgroup = true/' /etc/containerd/config.toml
sudo systemctl restart containerd.service
sudo systemctl restart kubelet.service
```
- This section is responsible for configuring Containerd, the container runtime used by Kubernetes:
  - It creates a directory, `/etc/containerd`, to store Containerd's configuration.
  - It updates the Containerd configuration in `/etc/containerd/config.toml` to ensure it uses systemd cgroups for managing containers.
  - It then writes the default Containerd configuration to the same file.
  - After these modifications, it restarts the Containerd service and the kubelet service.

### Step 8: Initialize the Kubernetes Cluster
```shell
sudo kubeadm config images pull
sudo kubeadm init --pod-network-cidr=10.10.0.0/16
```
- This step initializes the Kubernetes cluster:
  - `kubeadm config images pull` pre-pulls the necessary container images used by Kubernetes.
  - `kubeadm init` initializes the cluster with the specified Pod network CIDR, in this case, `10.10.0.0/16`.

### Step 9: Configure `kubectl` for the User
```shell
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
- This part prepares the `kubectl` command-line tool for the current user:
  - It creates the `~/.kube` directory to store `kubectl` configurations.
  - It copies the Kubernetes admin configuration to the user's home directory.
  - It adjusts the ownership of the `kubectl` configuration to match the user, ensuring that it can be used without superuser privileges.

### Step 10: Deploy Calico Network Plugin
```shell
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/tigera-operator.yaml
curl https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/custom-resources.yaml -O
sed -i 's/cidr: 192\.168\.0\.0\/16/cidr: 10.10.0.0\/16/g' custom-resources.yaml
kubectl create -f custom-resources.yaml
```
- This part deploys the Calico network plugin for Kubernetes networking:
  - It uses `kubectl` to create a Kubernetes resource from the Calico operator YAML file.
  - It downloads a custom resource definition (CRD) YAML file for Calico and adjusts the Pod network CIDR in the file.
  - It creates the custom resources using `kubectl`, effectively deploying Calico to handle networking within the cluster.

### Step 11: Join Worker Nodes
After completing the cluster

 initialization, you can run the following command on worker nodes to join them to the cluster:

```shell
kubeadm token create --print-join-command
```
- This command generates a token and join command. On the worker nodes, you can execute the join command to connect them to the newly created Kubernetes cluster.

Now you have a Kubernetes cluster up and running, ready for your containerized applications! Enjoy the power of Kubernetes 🚀🐳🛡🛠🌐🔒.

- `swapoff -`: Disables swap space.
- `sed -i '/ swap / s/^/#/' /etc/fstab`: Comments out swap entries in the `/etc/fstab` file to prevent automatic reactivation on system reboot.

## Step 2: Load Kernel Modules

```shell
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
    overlay
    br_netfilter
EOF
sudo modprobe overlay
sudo modprobe br_netfilter
```

- The script creates a configuration file for necessary kernel modules:
  - `overlay` and `br_netfilter` are required modules for Kubernetes networking.
- `modprobe` loads the specified kernel modules.

## Step 3: Configure sysctl Parameters

```shell
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
    net.bridge.bridge-nf-call-iptables  = 1
    net.bridge.bridge-nf-call-ip6tables = 1
    net.ipv4.ip_forward                 = 1
EOF
sudo sysctl --system
```

- This step configures sysctl parameters required for Kubernetes networking and forwarding.
- `sysctl --system` applies the settings without a reboot.

## Step 4: Set Up Package Management

```shell
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl
```

- Update the package list and install essential packages for repository management and secure downloads.

## Step 5: Add Kubernetes Repository

```shell
sudo mkdir /etc/apt/keyrings
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-archive-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
```

- This step adds the Kubernetes repository to the system's APT sources list.

## Step 6: Install Kubernetes and Docker

```shell
sudo apt install -y kubelet kubeadm kubectl
sudo apt install -y docker.io
```

- Installs Kubernetes components: `kubelet`, `kubeadm`, and `kubectl`.
- Installs Docker, the required container runtime for Kubernetes.

## Step 7: Configure Containerd

```shell
mkdir -p /etc/containerd
sudo sed -i 's/ SystemdCgroup = false/ SystemdCgroup = true/' /etc/containerd/config.toml
sudo sh -c "containerd config default > /etc/containerd/config.toml"
sudo sed -i 's/ SystemdCgroup = false/ SystemdCgroup = true/' /etc/containerd/config.toml
sudo systemctl restart containerd.service
sudo systemctl restart kubelet.service
```

- Creates a directory for containerd configuration.
- Configures containerd to use systemd cgroups.
- Restarts the containerd and kubelet services.

## Step 8: Initialize the Kubernetes Cluster

```shell
sudo kubeadm config images pull
sudo kubeadm init --pod-network-cidr=10.10.0.0/16
```

- Pulls the required container images for Kubernetes.
- Initializes the Kubernetes cluster with the specified Pod network CIDR.

## Step 9: Configure `kubectl` for the User

```shell
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

- Creates the `~/.kube` directory and configures `kubectl` for the current user.

## Step 10: Deploy Calico Network Plugin

```shell
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/tigera-operator.yaml
curl https://raw.githubusercontent.com/projectcalico/calico/v3.26.1/manifests/custom-resources.yaml -O
sed -i 's/cidr: 192\.168\.0\.0\/16/cidr: 10.10.0.0\/16/g' custom-resources.yaml
kubectl create -f custom-resources.yaml
```

- Deploys the Calico network plugin for Kubernetes networking.

## Step 11: Join Worker Nodes

After the cluster initialization, you can run the following command on worker nodes to join them to the cluster:

```shell
kubeadm token create --print-join-command
```

This command will generate a token and join command that you can use on worker nodes to join them to the cluster.