# 🌐 IPFS Web3 Portfolio Setup Guide

This guide explains how to update your decentralized portfolio site hosted on IPFS.

## 📂 New Content Created
I have generated the following asset for your IPFS site:
- **`architecture_map.html`**: An interactive, dark-mode visualization of your repository ecosystem.

## 🚀 How to Upload to IPFS

Since IPFS is immutable, "updating" means uploading a new folder containing your content and getting a new hash (CID).

### Option 1: Use a Pinning Service (Recommended)
1. **Pinata / Fleek / Web3.Storage**:
   - Log in to your pinning service dashboard.
   - Create a folder named `welshdog-portfolio`.
   - Add `architecture_map.html` to this folder.
   - Add an `index.html` (your main landing page).
   - Upload the **entire folder**.
   - Copy the new CID (Hash).

### Option 2: Use IPFS Desktop
1. Open IPFS Desktop app.
2. Click **Import** -> **Folder**.
3. Select your local folder containing `architecture_map.html`.
4. Share the returned Link/CID.

## 🔗 Updating Your Domains
Once you have the new CID (e.g., `bafy...newhash`):

1. **Update Unstoppable Domains / ENS**:
   - Point your `.crypto` or `.eth` domain to the new CID.

2. **Update GitHub Profile**:
   - I tried to automate this, but if it failed, manually edit your bio/website with the new gateway link:
     `https://ipfs.io/ipfs/YOUR_NEW_CID`

## 🛠️ Verification
After uploading, visit:
`https://ipfs.io/ipfs/YOUR_NEW_CID/architecture_map.html`

It should show the "Neurodivergent Dev Universe Map" with interactive nodes linking to your repos.
