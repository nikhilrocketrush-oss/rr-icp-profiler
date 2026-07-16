# Cowork + Claude in Chrome — daily DM workflow

Uses the recorded LinkedIn-inbox shortcut. References
messaging-framework.md for signal/message logic.

1. Open LinkedIn → Messaging tab.
2. Open the 20 most recent conversations.
3. For each conversation:
   - Client replied since your last message → classify green/red signal
     (messaging-framework.md). Red → mark "no further message." Green →
     draft the next message in the sequence (2 or 3, whichever is next).
   - No reply, and 3-5+ days passed → draft the no-reply follow-up
     (Option B, matched to parameter). Less than 3-5 days → skip, too soon.
4. Log every conversation as one row in an Excel sheet: Name | Profile URL
   | Last message sent | Client reply (if any) | Signal | Drafted next
   message | Status (Pending).
5. Show the sheet. Wait for each row to be marked Approved or edited.
6. For every Approved row: open that person's thread in LinkedIn, paste
   the drafted message, send.
