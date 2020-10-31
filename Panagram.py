"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import re                   # for pattern matching
import tkinter as tk        # for GUI
import tkinter.ttk as ttk   # for GUI
import tkinter.messagebox   # for showing error messages
import sys                  # for exit with error


number_of_found_words = 0   # store number of found words to show in status bar


def is_any_letter_in_string(letters_list, string):
    for letter in letters_list.split(","):  # consider each letter individually
        if letter in string.rstrip():
            return True
        else:
            continue
    return False


def do_all_letters_are_in_string(letters_list, string):
    for letter in letters_list.split(","):
        if string.find(letter) > 0:
            continue
        else:
            return False
    return True


def does_string_contain_only_letters_list(letters_list, string):
    # try to eliminate all letters in letters_list from string. if after all eliminations
    # anything remains it will return False
    for letter in letters_list.split(","):
        string = string.replace(letter, '')

    if string == '\n':
        return True
    else:
        return False


def results_clear():
    # reset number of found words
    global number_of_found_words
    number_of_found_words = 0
    # clear result output before populating it with new results
    listbox_result.delete(0, tk.END)
    # clear status bar
    statusbar.config(text="")


def update_gui():
    # refresh window after each insertion instead of waiting for all results
    main_window.update()


def results_insert(word):
    global number_of_found_words
    number_of_found_words += 1
    # update statusbar
    statusbar.config(text="word(s) found: " + str(number_of_found_words))
    # insert word
    listbox_result.insert(tk.END, word)


def reset_progressbar():
    progressbar_var.set(0)
    update_gui()


# GUI behaviour

def on_button_any_of_letters_in_word(event):
    # prevent listbox_result population with all dictionary while there is no input
    if not entry_var_user_input_letters.get():
        return

    results_clear()

    for index, word_from_dict in enumerate(dictionary_list, start=1):
        # update gui every 10% progress
        if ((100 * index / len(dictionary_list)) % 10) == 0:
            progressbar_var.set(index)
            update_gui()
        if is_any_letter_in_string(letters_list=entry_var_user_input_letters.get(), string=word_from_dict):
            results_insert(word_from_dict)
        else:
            continue
    reset_progressbar()


def on_button_all_letters_are_in_word(event):
    # for button sunk effect and dictionary search prevention when there is no input
    if not entry_var_user_input_letters.get():
        return

    results_clear()

    for index, word_from_dict in enumerate(dictionary_list, start=1):
        # update gui every 10% progress
        if ((100 * index / len(dictionary_list)) % 10) == 0:
            progressbar_var.set(index)
            update_gui()
        if do_all_letters_are_in_string(letters_list=entry_var_user_input_letters.get(), string=word_from_dict):
            results_insert(word_from_dict)
        else:
            continue
    reset_progressbar()


def on_button_word_contains_only_letters(event):
    # for button sunk effect and dictionary search prevention when there is no input
    if not entry_var_user_input_letters.get():
        return

    results_clear()
    for index, word_from_dict in enumerate(dictionary_list, start=1):
        # update gui every 10% progress
        if ((100 * index / len(dictionary_list)) % 10) == 0:
            progressbar_var.set(index)
            update_gui()
        if does_string_contain_only_letters_list(letters_list=entry_var_user_input_letters.get(),
                                                 string=word_from_dict):
            results_insert(word_from_dict)
        else:
            continue
    reset_progressbar()


def on_button_pattern_matching(event):
    # for button sunk effect and dictionary search prevention when there is no input
    if not entry_var_user_input_letters.get():
        return

    results_clear()

    for index, word_from_dict in enumerate(dictionary_list, start=1):
        # update gui every 10% progress
        if ((100 * index / len(dictionary_list)) % 10) == 0:
            progressbar_var.set(index)
            update_gui()
        if re.search(pattern='^'+entry_var_user_input_letters.get()+'$', string=word_from_dict):
            results_insert(word_from_dict)
        else:
            continue
    reset_progressbar()


# GUI design

main_window = tk.Tk()
main_window.title("Panagram")
main_window.resizable(width=False, height=False)

letters_input_label = tk.Label(master=main_window, text="Letter(s):")
letters_input_label.grid(row=0, column=0)

entry_var_user_input_letters = tk.StringVar()
entry_prime_check = tk.Entry(master=main_window, textvariable=entry_var_user_input_letters)
entry_prime_check.grid(row=0, column=1, columnspan=2, sticky=tk.E + tk.W)  # 'sticky' used to span entry

button_word_contains_only_letters = tk.Button(master=main_window)
button_word_contains_only_letters.config(text="Word contains only Letters")
button_word_contains_only_letters.bind("<ButtonRelease-1>", on_button_word_contains_only_letters)
button_word_contains_only_letters.grid(row=1, column=0)

button_all_letters_are_in_word = tk.Button(master=main_window)
button_all_letters_are_in_word.config(text="All Letters are in Word")
button_all_letters_are_in_word.bind("<ButtonRelease-1>", on_button_all_letters_are_in_word)
button_all_letters_are_in_word.grid(row=1, column=1)

button_any_of_letters_in_word = tk.Button(master=main_window)
button_any_of_letters_in_word.config(text="Any of Letter(s) in Word")
button_any_of_letters_in_word.bind("<ButtonRelease-1>", on_button_any_of_letters_in_word)
button_any_of_letters_in_word.grid(row=1, column=2)

button_pattern_matching = tk.Button(master=main_window)
button_pattern_matching.config(text="Pattern Matching")
button_pattern_matching.bind("<ButtonRelease-1>", on_button_pattern_matching)
button_pattern_matching.grid(row=2, column=0, sticky=tk.E + tk.W)

labelframe_result = tk.LabelFrame(master=main_window, text="Results")
labelframe_result.grid(row=3, column=0, columnspan=3, sticky=tk.E + tk.W)

listbox_result = tk.Listbox(master=labelframe_result)
listbox_result.pack(side=tk.LEFT, fill=tk.X, expand=True)

scroll_listbox_result = tk.Scrollbar(master=labelframe_result, command=listbox_result.yview, orient=tk.VERTICAL)
listbox_result.configure(yscrollcommand=scroll_listbox_result.set)
scroll_listbox_result.pack(side=tk.RIGHT, fill=tk.Y)

statusbar = tk.Label(master=main_window, relief=tk.SUNKEN, anchor=tk.W)
statusbar.grid(row=4, column=0, columnspan=1, sticky=tk.E + tk.W)


# open and parse dictionary file

try:
    dict_file = open("dictionary.txt")
except IOError as e:  # dictionary does not exists
    tkinter.messagebox.showerror(title="Error", message=e)
    sys.exit(e)
else:
    dictionary_list = dict_file.readlines()
    dict_file.close()

progressbar_var = tk.DoubleVar(master=main_window)
progressbar = ttk.Progressbar(master=main_window, orient=tk.HORIZONTAL, variable=progressbar_var,
                              maximum=len(dictionary_list), mode='determinate')
progressbar.grid(row=4, column=1, columnspan=2, sticky=tk.E + tk.W)

# enter main loop

main_window.mainloop()
