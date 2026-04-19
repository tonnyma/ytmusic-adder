"""
YouTube Music Playlist Auto-Adder
==================================
Searches for songs and adds them to your YouTube Music playlist.

FIRST TIME SETUP:
  1. pip install -r requirements.txt
  2. ytmusicapi oauth        ← opens browser to sign in with Google
  3. python add_to_playlist.py

AFTER THAT:
  Just edit SONGS below and run:  python add_to_playlist.py
"""

from ytmusicapi import YTMusic
import time

# ─── YOUR CONFIG ─────────────────────────────────────────────────────────────

PLAYLIST_ID = "PLwHQDN8d38CkN6bkEKDyZ3sElDXD_RcEc"  # Your "Test" playlist

SONGS = [
    # New Songs — from your top artists
    "Satellites - Above & Beyond",
    "Haunted Heart - Tove Lo",
    "Ghost In The Machine - Armin van Buuren",
    "Stardust - Max Oazo",
    "Drift - Gorgon City",
    "Burn the Night - Tiesto",
    "Free Fall - Kaskade",
    "Run - RAYE",
    "Cascade - Nora En Pure",
    "Again Again - Anyma",
    "How Do I Know - Lane 8",
    "Wavelength - Above Beyond",
]

DELAY_BETWEEN_ADDS = 1.5   # seconds — avoids rate limits
SONGS_ONLY = True           # True = prefer songs over music videos

# ─────────────────────────────────────────────────────────────────────────────

def find_video_id(yt, query):
    try:
        filter_type = "songs" if SONGS_ONLY else None
        results = yt.search(query, filter=filter_type, limit=5)
        if not results:
            results = yt.search(query, limit=5)
        if results:
            top = results[0]
            vid = top.get("videoId")
            title = top.get("title", "?")
            artists = ", ".join(a["name"] for a in (top.get("artists") or []))
            return vid, f"{title} — {artists}"
    except Exception as e:
        print(f"  ⚠  Search error: {e}")
    return None, None


def main():
    print()
    print("━" * 52)
    print("  🎵  YouTube Music Playlist Auto-Adder")
    print("━" * 52)

    # Auth
    try:
        yt = YTMusic("oauth.json")
        print("✓  Authenticated\n")
    except FileNotFoundError:
        print("\n✗  oauth.json not found.")
        print("   Run this first:\n")
        print("     ytmusicapi oauth\n")
        print("   Then re-run this script.")
        return

    # Confirm playlist
    try:
        info = yt.get_playlist(PLAYLIST_ID, limit=1)
        title = info.get("title", "Unknown")
        count = info.get("trackCount", "?")
        print(f"✓  Playlist: \"{title}\"  ({count} tracks currently)")
        print(f"   Adding {len(SONGS)} songs...\n")
    except Exception as e:
        print(f"✗  Can't access playlist: {e}")
        print("   Double-check PLAYLIST_ID and your account access.")
        return

    added, skipped = [], []

    for i, query in enumerate(SONGS, 1):
        print(f"  [{i:02d}/{len(SONGS)}]  {query}")
        vid, matched = find_video_id(yt, query)

        if not vid:
            print(f"          ✗ Not found — skipped\n")
            skipped.append(query)
            continue

        print(f"          ↳ {matched}")

        try:
            res = yt.add_playlist_items(PLAYLIST_ID, [vid])
            if res and res.get("status") == "STATUS_SUCCEEDED":
                print(f"          ✓ Added!\n")
                added.append(query)
            else:
                print(f"          ⚠ Unexpected response — skipped\n")
                skipped.append(query)
        except Exception as e:
            print(f"          ✗ Error: {e}\n")
            skipped.append(query)

        time.sleep(DELAY_BETWEEN_ADDS)

    # Summary
    print("━" * 52)
    print(f"  Done!  {len(added)}/{len(SONGS)} songs added successfully.")
    if skipped:
        print(f"\n  Skipped ({len(skipped)}):")
        for s in skipped:
            print(f"    ·  {s}")
    print()
    print(f"  Open playlist:")
    print(f"  https://music.youtube.com/playlist?list={PLAYLIST_ID}")
    print("━" * 52)


if __name__ == "__main__":
    main()
