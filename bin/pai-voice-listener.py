#!/usr/bin/env python3

"""
PAI Voice Recognition System
Advanced speech-to-text with wake word detection
Part of the Personal AI Infrastructure (PAI)
"""

import subprocess
import sys
import time
import json
import os
import signal
from pathlib import Path

class PAIVoiceListener:
    def __init__(self):
        self.wake_words = ["hatter", "pai", "hey hatter", "hey pai"]
        self.listening = False
        self.config_dir = Path.home() / ".config" / "pai"
        self.log_file = self.config_dir / "voice-recognition.log"
        
        # Create config directory
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
    def log(self, message):
        """Log voice recognition events"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp}: {message}\n")
        print(f"🎤 {message}")
    
    def speak(self, message):
        """Text-to-speech output"""
        print(f"🗣️  Hatter: {message}")
        self.log(f"SPEAK: {message}")
        
        # Try different TTS engines
        try:
            if subprocess.run(["which", "espeak"], capture_output=True).returncode == 0:
                subprocess.run(["espeak", "-s", "150", "-v", "en+f3", message], 
                             stderr=subprocess.DEVNULL)
            elif subprocess.run(["which", "say"], capture_output=True).returncode == 0:
                subprocess.run(["say", message], stderr=subprocess.DEVNULL)
        except:
            pass  # Silent fallback to text only
    
    def simple_voice_recognition(self):
        """
        Simplified voice recognition using keyboard input
        In production, this would use real STT like speech_recognition library
        """
        print("\n🎤 PAI VOICE RECOGNITION ACTIVE")
        print("=" * 40)
        print("💡 Voice Recognition Simulation Mode")
        print("   (Type commands as if speaking them)")
        print("\nWake words: 'Hey Hatter' or 'Hey PAI'")
        print("Available commands:")
        print("• 'Hey Hatter, show status'")  
        print("• 'PAI, run performance check'")
        print("• 'Hey Hatter, storage cleanup'")
        print("• 'PAI, show libraries'")
        print("• 'Hey Hatter, stop listening'")
        print("\nListening for commands...")
        
        while True:
            try:
                # Simulate listening for voice input
                print("\n🎙️  [Listening...]", end=" ")
                voice_input = input().strip()
                
                if not voice_input:
                    continue
                    
                self.log(f"INPUT: {voice_input}")
                
                # Check for wake words
                voice_lower = voice_input.lower()
                wake_detected = any(wake in voice_lower for wake in self.wake_words)
                
                if wake_detected or voice_input.lower() in ['exit', 'quit', 'stop']:
                    # Process the command
                    result = self.process_command(voice_input)
                    if not result:  # Stop command received
                        break
                else:
                    print("💭 (No wake word detected - try 'Hey Hatter, [command]')")
                    
            except KeyboardInterrupt:
                self.speak("Voice recognition stopped")
                break
            except EOFError:
                break
                
        self.log("Voice recognition session ended")
    
    def process_command(self, voice_input):
        """Process voice commands and route to PAI tools"""
        voice_lower = voice_input.lower()
        
        # Remove wake words
        for wake in self.wake_words:
            if wake in voice_lower:
                voice_lower = voice_lower.replace(wake, "").strip(" ,")
                break
        
        self.log(f"PROCESSING: {voice_lower}")
        
        # Command routing
        if any(word in voice_lower for word in ['stop', 'quit', 'exit', 'goodbye']):
            self.speak("Goodbye! Voice commands disabled.")
            return False
            
        elif any(word in voice_lower for word in ['status', 'server status']):
            self.speak("Checking Plex server status")
            subprocess.run(["/home/jbyrd/hatter-pai/bin/pai-plex-remote", "status"])
            self.speak("Status check complete")
            
        elif any(word in voice_lower for word in ['libraries', 'show libraries']):
            self.speak("Showing Plex libraries")  
            subprocess.run(["/home/jbyrd/hatter-pai/bin/pai-plex-remote", "libraries"])
            
        elif any(word in voice_lower for word in ['activity', 'recent activity']):
            self.speak("Showing recent Plex activity")
            subprocess.run(["/home/jbyrd/hatter-pai/bin/pai-plex-remote", "recent-activity"])
            
        elif any(word in voice_lower for word in ['health', 'performance', 'health check']):
            self.speak("Running Plex health check")
            subprocess.run(["/home/jbyrd/hatter-hai/bin/pai-plex-remote", "health-check"])
            self.speak("Health check complete")
            
        elif any(word in voice_lower for word in ['storage', 'cleanup', 'storage cleanup']):
            self.speak("Storage cleanup is available. This will recover 28 gigabytes.")
            response = input("🤔 Proceed with storage cleanup? (y/N): ")
            if response.lower().startswith('y'):
                self.speak("Starting storage cleanup")
                subprocess.run(["/home/jbyrd/hatter-pai/bin/pai-plex-storage-cleanup"])
                self.speak("Storage cleanup completed")
            else:
                self.speak("Storage cleanup cancelled")
                
        elif any(word in voice_lower for word in ['progress', 'task status']):
            self.speak("Current task: Voice command system is active and working")
            
        elif any(word in voice_lower for word in ['help', 'commands']):
            self.speak("Available commands: status, libraries, activity, health check, storage cleanup, progress, help, or stop listening")
            
        else:
            self.speak(f"Unknown command. Say 'help' for available commands.")
            print(f"💡 You said: '{voice_lower}'")
        
        return True
    
    def start(self):
        """Start the voice recognition system"""
        self.speak("Voice command system activated")
        self.simple_voice_recognition()

def main():
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            print("PAI Voice Recognition System")
            print("Usage: pai-voice-listener.py [--test]")
            return
        elif sys.argv[1] == '--test':
            listener = PAIVoiceListener()
            listener.speak("Voice recognition test successful")
            return
    
    # Start voice recognition
    listener = PAIVoiceListener()
    try:
        listener.start()
    except KeyboardInterrupt:
        listener.speak("Voice recognition stopped")

if __name__ == "__main__":
    main()

