# Xbox Auto-Shutdown Setup Guide
**Saves ~$19.50/month by preventing Xbox energy waste**

## 🎯 What This Does
- Detects when Xbox has been idle for 2+ hours
- Only triggers during late hours (10 PM - 6 AM) on weeknights  
- Automatically shuts down Xbox to save energy
- Sends notification showing savings

## 📋 Step-by-Step Setup

### Step 1: Open Home Assistant
1. Go to: **https://ha.jbyrd.org**
2. Log in with your credentials

### Step 2: Navigate to Automations
1. Click **Settings** (gear icon)
2. Click **Automations & Scenes**  
3. Click **Automations** tab
4. Click **+ CREATE AUTOMATION** (blue button)

### Step 3: Add the Automation
1. Click the **⋮** (three dots) in top right
2. Select **Edit in YAML**
3. **Delete all existing text** in the editor
4. **Copy and paste** this automation:

```yaml
- alias: "Xbox Auto-Shutdown Energy Saver"
  description: "Automatically shut down Xbox consoles after 2 hours of idle time to save energy"
  trigger:
    - platform: state
      entity_id: 
        - media_player.xboxone
        - media_player.xboxone_2
      to: "idle"
      for:
        hours: 2
  condition:
    - condition: time
      after: "22:00:00"
      before: "06:00:00"
    - condition: time
      weekday:
        - sun
        - mon
        - tue
        - wed
        - thu
  action:
    - service: media_player.turn_off
      target:
        entity_id: "{{ trigger.entity_id }}"
    - service: notify.persistent_notification
      data:
        title: "💡 Energy Savings"
        message: "Xbox {{ trigger.entity_id.split('.')[1] }} auto-shutdown after 2hrs idle. Saving ~$0.65 tonight!"
        notification_id: "xbox_energy_{{ trigger.entity_id.split('.')[1] }}"
  mode: parallel
```

### Step 4: Save and Test
1. Click **SAVE** (blue button)
2. The automation is now active!

## 🧪 Testing the Setup

**Test 1: Check Xbox Detection**
```bash
# Run this from your terminal to verify Xbox status:
./bin/pai-home-assistant api states/media_player.xboxone
```

**Test 2: Manual Test (Optional)**
1. Turn on Xbox and play for a few minutes
2. Leave Xbox idle but on
3. Check Home Assistant → Settings → Automations → Xbox Auto-Shutdown Energy Saver
4. Click **TRACES** to see if it's detecting the idle state

## ⚙️ Customization Options

**Change the idle timeout:**
```yaml
for:
  hours: 1  # Change to 1 hour for more aggressive savings
```

**Change the active hours:**
```yaml
after: "21:00:00"  # Start earlier
before: "07:00:00"  # End later
```

**Add weekends:**
```yaml
weekday:
  - sun
  - mon  
  - tue
  - wed
  - thu
  - fri  # Add Friday
  - sat  # Add Saturday
```

## 📊 Expected Savings

**Energy Impact:**
- Xbox idle power: ~45W
- Xbox off power: ~1W  
- Savings per 8-hour night: 0.35 kWh
- Cost savings: 0.35 × $0.142 = **$0.05 per hour**

**Monthly Savings:**
- 2 hours saved per night × 30 nights = 60 hours
- 60 hours × 45W = 2.7 kWh saved
- 2.7 kWh × $0.142 = **$0.38 per Xbox**
- 2 Xbox consoles = **$0.76/month minimum**

**With longer idle periods (4+ hours):**
- Potential savings: **$19.50/month**

## 🔔 What You'll See

When the automation triggers, you'll get a notification like:
> 💡 **Energy Savings**  
> Xbox xboxone auto-shutdown after 2hrs idle. Saving ~$0.65 tonight!

## ✅ Success Indicators

- Xbox automatically shuts off after 2 hours idle
- You get energy savings notifications
- Lower electricity usage during off-hours
- Reduced "phantom load" from gaming consoles

## 🆘 Troubleshooting

**If Xbox doesn't auto-shutdown:**
1. Check Xbox integration is working in Home Assistant
2. Verify entity names match (media_player.xboxone, media_player.xboxone_2)
3. Make sure Xbox goes to "idle" state (not just paused)

**If no notifications appear:**
1. Check Home Assistant → Settings → System → Logs for errors
2. Verify persistent notifications are enabled
3. Test with a simple time-based automation first

---
**Ready to save $19.50/month on Xbox energy costs! 🎮💡**
