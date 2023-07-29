
#Online ELection System Simple GUI Based to cast votes, register voters, and show result of the election

import hashlib
import tkinter as tk
from tkinter import messagebox

# Global variable to hold the reference to the "Show Voters" button
button_show_voters = None
button_show_results = None

class Candidate:
    def __init__(self, name, party):
        self.name = name
        self.party = party
        self.votes = 0

class Voter:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

class Election:
    def __init__(self, candidates):
        self.candidates = candidates
        self.voters = {}
        self.vote_count = 0

    def add_voter(self, username, password):
        if username not in self.voters:
            self.voters[username] = Voter(username, password)
            messagebox.showinfo("Success", "Voter registered successfully!")
            if len(self.voters) >= 1:
                button_show_voters.config(state=tk.NORMAL)  # Enable the "Show Voters" button

    def vote(self, username, candidate_index):  
        if username in self.voters:
            voter = self.voters[username]
            if candidate_index == 0:
                messagebox.showinfo("Info", "Please select a candidate.")
            elif 0 < candidate_index <= len(self.candidates):
                candidate = self.candidates[candidate_index]
                candidate.votes += 1
                self.vote_count += 1
                messagebox.showinfo("Success", f"Vote casted for {candidate.name} ({candidate.party})")
                if self.vote_count >= 3:
                    button_show_results.config(state=tk.NORMAL)  # Enable the "Show Results" button
            else:
                messagebox.showerror("Error", "Invalid candidate index.")
        else:
            messagebox.showerror("Error", "Invalid voter credentials.")

    def get_results(self):
        if self.vote_count < 3:
            messagebox.showinfo("Info", "At least 3 votes are required to show results.")
            return

        sorted_candidates = sorted(self.candidates[1:], key=lambda candidate: candidate.votes, reverse=True)
        winner_party = sorted_candidates[0].party
        if sorted_candidates[0].votes == sorted_candidates[1].votes:
            winner_party = "No winner"

        winner_name = next((candidate.name for candidate in sorted_candidates if candidate.party == winner_party), "Unknown")

        results = "\n".join(f"{candidate.name} ({candidate.party}): {candidate.votes} votes" for candidate in sorted_candidates)
        results += f"\n\nWinning Candidate - {winner_name} ({winner_party})"
        messagebox.showinfo("Election Results", results)

def main():
    candidates = [
        Candidate("Select", "Select"),
        Candidate("Mayawati", "BSP"),
        Candidate("Narendra Modi", "BJP"),
        Candidate("Rahul Gandhi", "INC")
    ]

    election = Election(candidates)

    def set_button_show_voters(button):
        global button_show_voters
        button_show_voters = button

    def set_button_show_results(button):
        global button_show_results
        button_show_results = button
        button_show_results.config(state=tk.DISABLED)  # Disable the "Show Results" button initially

    def register_voter():
        username = entry_username.get().strip()
        password = entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Both username and password are required.")
        else:
            election.add_voter(username, password)

    def cast_vote():
        global button_show_results  # Use the global variable
        username = entry_username.get().strip()
        password = entry_password.get()
        candidate_name = var_candidate.get()
        if candidate_name in candidate_index_mapping:
            candidate_index = candidate_index_mapping[candidate_name]
            election.vote(username, candidate_index)
            if button_show_results and election.vote_count >= 3:
                button_show_results.config(state=tk.NORMAL)  # Enable the "Show Results" button
        else:
            messagebox.showerror("Error", "Invalid candidate selection.")

    def show_results():
        election.get_results()

    def show_voters():
        voters_list = "\n".join(voter.username for voter in election.voters.values())
        messagebox.showinfo("Registered Voters", voters_list)

    def on_dropdown_click(event):
        menu.delete(0, tk.END)
        for candidate in candidates[1:]:
            menu.add_command(label=f"{candidate.name} ({candidate.party})", command=lambda c=candidate: var_candidate.set(c.party))
        menu.post(dropdown_frame.winfo_rootx(), dropdown_frame.winfo_rooty() + dropdown_frame.winfo_height())

    root = tk.Tk()
    root.title("Online Election System")
    root.geometry("500x350")
    root.configure(bg="light coral")

    label_username = tk.Label(root, text="Username:", bg="light coral")
    label_username.pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    label_password = tk.Label(root, text="Password:", bg="light coral")
    label_password.pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    label_candidate = tk.Label(root, text="Select Candidate:", bg="light coral")
    label_candidate.pack(pady=(5, 0))

    var_candidate = tk.StringVar(root)
    var_candidate.set("Select")  

    dropdown_frame = tk.Frame(root, relief="solid", bd=1)
    dropdown_frame.pack(pady=5, padx=5)

    def toggle_dropdown():
        if menu.winfo_ismapped():
            menu.unpost()
        else:
            menu.delete(0, tk.END)
            for candidate in candidates[1:]:
                menu.add_command(label=f"{candidate.name} ({candidate.party})", command=lambda c=candidate: var_candidate.set(c.party))
            x = root.winfo_x() + dropdown_frame.winfo_x() + dropdown_frame.winfo_width() // 2
            y = root.winfo_y() + dropdown_frame.winfo_y() - dropdown_frame.winfo_height()
            menu.post(x, y)

    button_selected_candidate = tk.Button(dropdown_frame, textvariable=var_candidate, command=toggle_dropdown, relief="raised", bd=1, bg="lightblue")
    button_selected_candidate.pack(side=tk.LEFT)

    arrow_label = tk.Label(dropdown_frame, text="▼", cursor="hand2")
    arrow_label.pack(side=tk.RIGHT)
    arrow_label.bind("<Button-1>", on_dropdown_click)

    candidate_index_mapping = {candidate.party: i for i, candidate in enumerate(candidates)}

    menu = tk.Menu(root, tearoff=0)

    button_register_voter = tk.Button(root, text="Register Voter", command=register_voter, relief="solid", bd=1, bg="lightblue")
    button_register_voter.pack(pady=5)

    button_cast_vote = tk.Button(root, text="Cast Vote", command=cast_vote, relief="solid", bd=1, bg="lightblue", fg="black")
    button_cast_vote.pack(pady=5)

    button_show_results = tk.Button(root, text="Show Results", command=show_results, state=tk.DISABLED, relief="solid", bd=1, bg="lightblue")
    button_show_results.pack(pady=5)

    button_show_voters = tk.Button(root, text="Show Voters", command=show_voters, state=tk.DISABLED, relief="solid", bd=1, bg="lightblue")
    button_show_voters.pack(pady=5)

    set_button_show_voters(button_show_voters)  # Set the reference for the "Show Voters" button
    set_button_show_results(button_show_results)  # Set the reference for the "Show Results" button

    root.mainloop()

if __name__ == "__main__":
    main()
