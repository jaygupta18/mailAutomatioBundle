

import requests
import json

def test_settings_integration():
  
    test_settings = {
        "action": "process_emails",
        "settings": {
            "maxEmails": "5",
            "replyStyle": "casual",
            "customPrompt": "Always include a smiley face in your replies"
        }
    }
    
    print("🧪 Testing settings integration...")
    print(f"📤 Sending settings: {json.dumps(test_settings, indent=2)}")
    
    try:
        
        health_response = requests.get("http://localhost:5000/health")
        if health_response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server health check failed")
            return False
        
        
        response = requests.post(
            "http://localhost:5000/process-emails",
            headers={"Content-Type": "application/json"},
            json=test_settings
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Settings integration test passed!")
            print(f"📊 Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_settings_integration()
    if success:
        print("\n🎉 All settings integration tests passed!")
    else:
        print("\n💥 Settings integration tests failed!")
