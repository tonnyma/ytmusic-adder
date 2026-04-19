# 🎵 YouTube Music Playlist Auto-Adder

Automatically searches and adds songs to your YouTube Music playlist — runs entirely in the browser via GitHub Codespaces. No laptop needed.

---

## iPhone Setup (one-time, ~5 minutes)

### Step 1 — Fork this repo
1. Open this repo on GitHub in Safari
2. Tap **Fork** (top right) → **Create fork**
3. You now have your own copy at `github.com/YOUR-USERNAME/ytmusic-adder`

### Step 2 — Open in Codespaces
1. On your forked repo, tap the green **`<> Code`** button
2. Tap **Codespaces** tab
3. Tap **Create codespace on main**
4. Wait ~60 seconds — a full terminal opens in your browser
5. Dependencies install automatically (`ytmusicapi` is ready to go)

### Step 3 — Authenticate with Google (one-time)
In the terminal that opens, run:
```bash
ytmusicapi oauth
```
- It prints a URL — **copy and open it** in a new Safari tab
- Sign in with the Google account linked to your YouTube Music
- After signing in, paste the redirect URL back into the terminal
- This saves `oauth.json` — your auth token (stays in Codespaces, never committed to GitHub)

### Step 4 — Run the adder
```bash
python add_to_playlist.py
```
Watch it search and add each song live. Done! ✓

---

## Adding different songs

Edit `add_to_playlist.py` in the Codespaces editor:

1. Find the `SONGS = [...]` list near the top
2. Edit, add, or remove songs in `"Song Title - Artist"` format
3. Save (⌘S or Ctrl+S)
4. Run again: `python add_to_playlist.py`

To change the playlist, update `PLAYLIST_ID` with the ID from your YouTube Music playlist URL.

---

## Next time (returning to Codespaces)

1. Go to [github.com/codespaces](https://github.com/codespaces)
2. Tap your existing `ytmusic-adder` codespace to reopen it
3. `oauth.json` is still there — no need to re-authenticate
4. Just run: `python add_to_playlist.py`

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `oauth.json not found` | Run `ytmusicapi oauth` again |
| Song not found | Try a simpler search string, e.g. `"Blinding Lights - Weeknd"` |
| Playlist access error | Make sure you're signed into the right Google account |
| Codespace expired | Codespaces sleep after 30 min inactivity but `oauth.json` persists — just reopen |

---

## How it works

1. Authenticates as you via Google OAuth (your cookies, your account)
2. Searches YouTube Music for each song in your list
3. Grabs the top matching video ID
4. Calls `add_playlist_items()` on your playlist
5. Waits 1.5s between adds to avoid rate limits
