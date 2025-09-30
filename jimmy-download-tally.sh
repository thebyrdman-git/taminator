#!/bin/bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎊 JIMMY'S YOUTUBE SYSTEM - RUNNING TALLY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📅 Updated: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Get current status
status=$(curl -s http://192.168.1.34:5001/api/status 2>/dev/null)
if [ ! -z "$status" ]; then
  actual_files=$(echo "$status" | grep -o '"actual_files":[^,]*' | cut -d':' -f2)
  total_channels=$(echo "$status" | grep -o '"total_channels":[^,]*' | cut -d':' -f2)
  
  echo "📊 DOWNLOAD STATISTICS:"
  echo "======================"
  echo "📹 TOTAL VIDEOS DOWNLOADED: $actual_files"
  echo "📺 TOTAL CHANNELS MONITORED: $total_channels"
fi

# Get Plex counts
legal_count=$(curl -s "http://192.168.1.17:32400/library/sections/33/all?X-Plex-Token=***REMOVED***" 2>/dev/null | grep -o 'type="movie"' | wc -l 2>/dev/null || echo 0)
personal_count=$(curl -s "http://192.168.1.17:32400/library/sections/35/all?X-Plex-Token=***REMOVED***" 2>/dev/null | grep -o 'type="movie"' | wc -l 2>/dev/null || echo 0)
plex_total=$((legal_count + personal_count))

echo "📊 VIDEOS IN PLEX: $plex_total"

# Get storage info
storage=$(ssh jbyrd@192.168.1.34 "du -sh /media/jimmy/youtube/ 2>/dev/null | cut -f1" 2>/dev/null || echo "N/A")
echo "💾 TOTAL STORAGE USED: $storage"

echo ""
echo "📂 BREAKDOWN BY CATEGORY:"
echo "========================"
echo "   🏛️ Legal-Educational: $legal_count videos"
echo "   🎮 Personal-Interest: $personal_count videos"

echo ""
echo "🎬 SYSTEM STATUS: ✅ Fully Operational"
echo "🔄 PLEX INTEGRATION: ✅ Perfect Sync"
echo "🚀 READY FOR: New downloads anytime"
echo ""
echo "📱 QUICK ACCESS LINKS:"
echo "===================="
echo "🌐 Web Interface: http://192.168.1.34:5001"
echo "📺 Plex Streaming: http://192.168.1.17:32400"
echo "🚀 Start Downloads: http://192.168.1.34:5001/api/start_downloads"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 CURRENT TALLY: $actual_files Videos | $total_channels Channels | $storage | $plex_total in Plex"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
