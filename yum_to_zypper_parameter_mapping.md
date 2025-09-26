# Parameter Mapping: yum_repository → zypper_repository

## ❌ **NO - Parameters are NOT the same!**

While both modules manage repositories, they have **different parameter names and behaviors** due to the underlying package manager differences.

## 📊 **Parameter Comparison Table**

| yum_repository | zypper_repository | Notes |
|----------------|-------------------|-------|
| `baseurl` | `repo` | ⚠️ **NAME CHANGE** |
| `name` | `name` | ✅ Same |
| `description` | `description` | ✅ Same |
| `enabled` | `enabled` | ✅ Same (boolean) |
| `gpgcheck` | `disable_gpg_check` | ⚠️ **LOGIC INVERTED** |
| `gpgkey` | `auto_import_keys` | ⚠️ **DIFFERENT BEHAVIOR** |
| `state` | `state` | ✅ Same |
| `file` | N/A | ❌ Not available |
| `mirrorlist` | N/A | ❌ Not available |
| `metalink` | N/A | ❌ Not available |
| `cost` | `priority` | ⚠️ **DIFFERENT CONCEPT** |
| N/A | `autorefresh` | ✅ New option |
| N/A | `runrefresh` | ✅ New option |

## 🔄 **Migration Examples**

### **Before (yum_repository):**
```yaml
- name: Add YUM repository
  yum_repository:
    name: custom-repo
    baseurl: https://example.com/repo/
    description: "Custom Repository"
    enabled: yes
    gpgcheck: yes
    gpgkey: https://example.com/key.gpg
    state: present
```

### **After (zypper_repository):**
```yaml
- name: Add Zypper repository  
  community.general.zypper_repository:
    name: custom-repo
    repo: https://example.com/repo/          # baseurl → repo
    description: "Custom Repository" 
    enabled: yes
    disable_gpg_check: no                   # gpgcheck: yes → disable_gpg_check: no
    auto_import_keys: yes                   # Handle GPG keys differently
    autorefresh: yes                        # New SUSE-specific option
    state: present
```

## ⚠️ **Key Differences to Watch:**

### **1. URL Parameter:**
- `yum_repository`: `baseurl`
- `zypper_repository`: `repo`

### **2. GPG Check Logic:**
- `yum_repository`: `gpgcheck: yes` (enable checking)
- `zypper_repository`: `disable_gpg_check: no` (don't disable = enable)

### **3. GPG Key Handling:**
- `yum_repository`: `gpgkey: [URL]` (specify key location)
- `zypper_repository`: `auto_import_keys: yes` (auto-import from repo)

### **4. SUSE-Specific Options:**
```yaml
autorefresh: yes        # Auto-refresh metadata (SUSE only)
runrefresh: yes         # Trigger immediate refresh
priority: 99            # Repository priority (lower = higher priority)
```

## 🚨 **Migration Checklist:**

- [ ] Change `baseurl` → `repo`
- [ ] Change `gpgcheck: yes` → `disable_gpg_check: no`
- [ ] Replace `gpgkey` with `auto_import_keys: yes`
- [ ] Add `autorefresh: yes` for SUSE best practices
- [ ] Update module name to `community.general.zypper_repository`
- [ ] Test on development system first
- [ ] Verify repository files created in `/etc/zypp/repos.d/`

## 📋 **Complete Migration Template:**

```yaml
# OLD - yum_repository
- name: Add repository (RHEL)
  yum_repository:
    name: "{{ repo_name }}"
    baseurl: "{{ repo_url }}"
    description: "{{ repo_description }}"
    enabled: "{{ repo_enabled }}"
    gpgcheck: "{{ repo_gpgcheck }}"
    gpgkey: "{{ repo_gpgkey }}"
    state: present
  when: ansible_os_family == "RedHat"

# NEW - zypper_repository  
- name: Add repository (SUSE)
  community.general.zypper_repository:
    name: "{{ repo_name }}"
    repo: "{{ repo_url }}"                    # baseurl → repo
    description: "{{ repo_description }}"
    enabled: "{{ repo_enabled }}"
    disable_gpg_check: "{{ not repo_gpgcheck }}"  # Inverted logic
    auto_import_keys: "{{ repo_gpgcheck }}"       # Different approach
    autorefresh: yes                              # SUSE best practice
    state: present
  when: ansible_os_family == "Suse"
```

## 💡 **Pro Tips:**

1. **Test parameter mapping** on development systems first
2. **Use conditionals** to support both RHEL and SUSE in same playbook
3. **Check repository creation** in `/etc/zypp/repos.d/` after migration
4. **Enable autorefresh** for SUSE systems to keep metadata current
5. **Consider priority settings** for repository precedence

---
**Bottom Line**: You **CANNOT** just swap module names - parameters need careful migration!
