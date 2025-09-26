# Package Management Migration: yum → zypper

## 🔄 **Module Replacement**

| RHEL/CentOS | SUSE Liberty Linux |
|-------------|-------------------|
| `ansible.builtin.yum` | `community.general.zypper` |

## 📊 **Parameter Comparison**

### **Common Parameters (Same Names):**
| Parameter | yum | zypper | Notes |
|-----------|-----|--------|-------|
| `name` | ✅ | ✅ | Package name(s) |
| `state` | ✅ | ✅ | present/absent/latest |
| `list` | ✅ | ✅ | List packages |

### **Different/Additional Parameters:**

| yum Parameter | zypper Equivalent | Notes |
|---------------|-------------------|-------|
| `enablerepo` | N/A | Use `zypper_repository` separately |
| `disablerepo` | N/A | Use `zypper_repository` separately |
| `update_cache` | `update_cache` | ✅ Same name, same function |
| `validate_certs` | N/A | Not available |
| N/A | `disable_recommends` | ⭐ **SUSE-specific**: Don't install recommended packages |
| N/A | `force` | ⭐ **SUSE-specific**: Force package operations |
| N/A | `oldpackage` | ⭐ **SUSE-specific**: Allow downgrades |

## 🔄 **Migration Examples**

### **1. Basic Package Installation**

**Before (yum):**
```yaml
- name: Install packages
  ansible.builtin.yum:
    name:
      - httpd
      - wget
      - curl
    state: present
```

**After (zypper):**
```yaml
- name: Install packages
  community.general.zypper:
    name:
      - apache2     # Note: Different package name!
      - wget
      - curl
    state: present
```

### **2. Update Cache + Install**

**Before (yum):**
```yaml
- name: Update cache and install
  ansible.builtin.yum:
    name: nginx
    state: present
    update_cache: yes
```

**After (zypper):**
```yaml
- name: Update cache and install
  community.general.zypper:
    name: nginx
    state: present
    update_cache: yes       # Same parameter name!
```

### **3. Install Latest Version**

**Before (yum):**
```yaml
- name: Install latest version
  ansible.builtin.yum:
    name: kernel
    state: latest
```

**After (zypper):**
```yaml
- name: Install latest version
  community.general.zypper:
    name: kernel-default    # Different kernel package name
    state: latest
```

### **4. Remove Packages**

**Before (yum):**
```yaml
- name: Remove packages
  ansible.builtin.yum:
    name:
      - httpd
      - mod_ssl
    state: absent
```

**After (zypper):**
```yaml
- name: Remove packages
  community.general.zypper:
    name:
      - apache2
      - apache2-mod_ssl
    state: absent
```

## ⭐ **SUSE-Specific Features**

### **1. Disable Recommendations**
```yaml
- name: Install without recommended packages
  community.general.zypper:
    name: package-name
    state: present
    disable_recommends: yes    # SUSE-only feature
```

### **2. Force Installation**
```yaml
- name: Force package installation
  community.general.zypper:
    name: package-name
    state: present
    force: yes                 # SUSE-only feature
```

### **3. Pattern Installation**
```yaml
- name: Install SUSE patterns
  community.general.zypper:
    name: 
      - pattern:lamp_server    # Install server patterns
      - pattern:devel_basis    # Development tools
    state: present
```

## 🚨 **Critical Package Name Differences**

| Service | RHEL Package | SUSE Package |
|---------|-------------|-------------|
| **Web Server** | `httpd` | `apache2` |
| **Kernel** | `kernel` | `kernel-default` |
| **SSH** | `openssh-server` | `openssh` |
| **Firewall** | `firewalld` | `firewalld` (same) |
| **Cron** | `cronie` | `cron` |
| **Development** | `gcc` | `gcc` (same) |

## 📋 **Complete Migration Template**

```yaml
---
- name: Package management (multi-distro)
  hosts: all
  vars:
    packages:
      RedHat:
        - httpd
        - mod_ssl
        - wget
      Suse:
        - apache2
        - apache2-mod_ssl  
        - wget

  tasks:
    # RHEL/CentOS systems
    - name: Install packages (RHEL)
      ansible.builtin.yum:
        name: "{{ packages.RedHat }}"
        state: present
        update_cache: yes
      when: ansible_os_family == "RedHat"

    # SUSE systems  
    - name: Install packages (SUSE)
      community.general.zypper:
        name: "{{ packages.Suse }}"
        state: present
        update_cache: yes
        disable_recommends: yes  # SUSE best practice
      when: ansible_os_family == "Suse"
```

## 🔧 **Prerequisites**

Before using `community.general.zypper`, install the collection:

```bash
ansible-galaxy collection install community.general
```

## ✅ **Migration Checklist**

- [ ] Replace `ansible.builtin.yum` → `community.general.zypper`
- [ ] Install `community.general` collection
- [ ] Update package names for SUSE equivalents
- [ ] Remove `enablerepo`/`disablerepo` (handle via `zypper_repository`)
- [ ] Consider adding `disable_recommends: yes`
- [ ] Test on development SUSE system
- [ ] Use `when: ansible_os_family == "Suse"` conditionals

## 💡 **Pro Tips**

1. **Package name research**: Use `zypper search package-name` to find SUSE equivalents
2. **Pattern installation**: Leverage SUSE patterns for software bundles
3. **Recommendations**: Consider `disable_recommends: yes` for minimal installs
4. **Multi-distro playbooks**: Use conditionals to support both RHEL and SUSE

---
**Bottom Line**: `community.general.zypper` is the direct replacement, but package names often differ!
