# BitTorrent Client - Testing Guide

## 🚀 Quick Start

### Option 1: Test with Ubuntu ISO (Recommended for beginners)

```bash
# 1. Download Ubuntu torrent file
curl -o ubuntu.torrent "https://releases.ubuntu.com/24.04/ubuntu-24.04.1-desktop-amd64.iso.torrent"

# 2. Run the client
node index.js ubuntu.torrent

# 3. Wait for download to complete
# The file will be saved as: ubuntu-24.04.1-desktop-amd64.iso
```

---

## 🧪 Testing on Two Devices

### Prerequisites
- Both devices on the same network (or Internet connection)
- Device 1: A BitTorrent client that can seed (qBittorrent/Transmission)
- Device 2: This Node.js client

### Device 1: Setup Seeder

1. **Install qBittorrent:**
   - macOS: `brew install qbittorrent`
   - Windows: Download from qbittorrent.org
   - Linux: `sudo apt install qbittorrent`

2. **Create a test file:**
   ```bash
   echo "Hello from Device 1!" > test.txt
   ```

3. **Create torrent in qBittorrent:**
   - Open qBittorrent
   - Tools → Torrent Creator
   - Select `test.txt`
   - Add tracker URL:
     ```
     http://tracker.opentrackr.org:1337/announce
     udp://tracker.openbittorrent.com:6969/announce
     ```
   - Save as `test.torrent`

4. **Start seeding:**
   - Add `test.torrent` to qBittorrent
   - Keep qBittorrent running

5. **Transfer torrent file to Device 2:**
   - Email, USB drive, or:
   ```bash
   # If both devices on same network:
   # Device 1:
   python3 -m http.server 8000
   
   # Device 2:
   curl -o test.torrent http://<device1-ip>:8000/test.torrent
   ```

### Device 2: Run Downloader

1. **Setup project:**
   ```bash
   git clone <your-repo-url>
   cd allen-torrent
   npm install
   ```

2. **Get the torrent file from Device 1**

3. **Run the client:**
   ```bash
   node index.js test.torrent
   ```

4. **Verify:**
   ```bash
   cat test.txt  # Should show "Hello from Device 1!"
   ```

---

## 🌐 Network Requirements

### Same Local Network:
- ✅ Easiest setup
- ✅ No firewall issues
- ✅ Fast transfers

### Over Internet:
- ⚠️ May need port forwarding on Device 1
- ⚠️ Firewall configuration
- Configure in qBittorrent: Tools → Options → Connection → Port

---

## 🔍 What Your Client Does

1. **Reads torrent file** → Gets tracker URL and file info
2. **Contacts tracker** → Asks "Who has this file?"
3. **Tracker responds** → Returns list of peers (IP:Port)
4. **Connects to peers** → Your client connects to seeders
5. **Downloads pieces** → Requests and downloads file chunks
6. **Verifies data** → Checks piece hashes
7. **Saves file** → Writes completed file to disk

---

## 📊 Expected Output

```
$ node index.js test.torrent

Connecting to peers...
0.00%
12.50%
25.00%
37.50%
50.00%
62.50%
75.00%
87.50%
100.00%
DONE!
```

---

## 🐛 Troubleshooting

### "No peers found"
- ✅ Check tracker URL is valid
- ✅ Ensure seeder is running
- ✅ Try public torrent (Ubuntu) to test

### "Connection refused"
- ✅ Check firewall settings
- ✅ Ensure seeder allows incoming connections
- ✅ Try same network first

### "File incomplete"
- ✅ Wait longer (seeder might be slow)
- ✅ Check if seeder has complete file
- ✅ Verify torrent file is correct

---

## 📚 Learn More

- **How BitTorrent works:** http://allenkim67.github.io/programming/2016/05/04/how-to-make-your-own-bittorrent-client.html
- **BitTorrent Protocol:** https://www.bittorrent.org/beps/bep_0003.html
