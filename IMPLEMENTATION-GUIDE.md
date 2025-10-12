# Smart Energy Scheduling Implementation Guide
**For 432-Device Smart Home Energy Optimization**

## 🎯 Target Savings: $30-60/month (15-25% reduction)

### Step 1: Add Schedules to Home Assistant

1. **Open Home Assistant**: https://ha.jbyrd.org
2. **Go to Settings** → Configuration → Automations & Scenes
3. **Click "+" to create new automation**
4. **Switch to YAML mode** (three dots → Edit in YAML)
5. **Copy and paste** each automation from `smart-schedule-config.yaml`

### Step 2: Priority Implementation Order

**🚀 Week 1 - Quick Wins (Est. $19/month savings)**
- [x] Xbox auto-shutdown automation (biggest impact)
- [x] Peak hours notifications  
- [x] Camera motion detection scheduling

**📈 Week 2 - Load Management (Est. $12/month savings)**  
- [x] Sequential device startup prevention
- [x] Load balancing for high power draw
- [x] Weekend gaming optimization

**💰 Week 3 - Advanced Monitoring (Est. $15/month savings)**
- [x] Daily usage alerts
- [x] Cost monitoring notifications
- [x] Off-peak hour reminders

### Step 3: Customization for Your Setup

**Adjust Timing Based on Your Schedule:**
```yaml
# Modify these times in the automations:
peak_hours: "17:00-21:00"      # Your most expensive electricity
off_peak: "23:00-06:00"        # Cheapest rates
sleep_mode: "22:00-06:00"      # Auto-shutdown window
```

**Customize Device Lists:**
```yaml
# Add your specific Xbox entities:
- media_player.xboxone
- media_player.xboxone_2
# Add any other high-power devices you discover
```

### Step 4: Monitoring & Optimization

**Track Your Savings:**
1. **Baseline**: Current 53.3 kWh/day average
2. **Target**: 40-45 kWh/day with smart scheduling  
3. **Monitor**: Use `pai-energy-optimize analyze` to track progress

**Weekly Check:**
```bash
# Run these commands weekly to monitor progress:
pai-energy-optimize costs
pai-home-assistant devices | grep -E "(xbox|media_player)"
```

### Step 5: Advanced Features (Optional)

**🤖 AI-Powered Scheduling**
- Use Home Assistant's machine learning to predict usage patterns
- Implement dynamic scheduling based on occupancy sensors
- Add weather-based optimizations for heating/cooling

**📱 Smart Notifications**
- Mobile alerts for high usage days
- Weekly energy reports
- Cost comparison with neighbors

## 🎊 Expected Results

**Month 1:**
- 15% usage reduction (8 kWh/day saved)
- $25-35/month cost reduction
- Better awareness of energy usage patterns

**Month 2-3:**
- 20-25% usage reduction (10-13 kWh/day saved)  
- $35-50/month cost reduction
- Automated optimization running smoothly

**Long-term:**
- Consistent 40-45 kWh/day usage (vs 53.3 kWh baseline)
- $420-600/year savings
- Smart home that manages its own energy consumption

## 🔧 Troubleshooting

**If Xbox won't auto-shutdown:**
- Check entity names match your specific Xbox devices
- Verify Xbox integration is working in HA
- Test manual shutdown commands first

**If notifications don't appear:**
- Enable persistent notifications in HA
- Check notification settings
- Test with a simple automation first

**If energy monitoring seems off:**
- Add more power monitoring devices
- Use smart plugs for unmonitored high-power devices
- Cross-reference with utility bill data

## 📞 Support Commands

```bash
# Check Home Assistant status
pai-home-assistant status

# Monitor energy costs
pai-energy-optimize costs

# View device status  
pai-home-assistant devices

# Generate monthly report
pai-energy-dashboard generate-report --export-format html
```

---

**Ready to save $30-60/month on your electricity bill with smart automation!**
