import argparse
import function as fc


def main():
    # parser initialization
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help='possible actions', dest='subparser')

    # PLOT argument
    plot_parser = subparsers.add_parser('plot', help='plot the data')
    plot_parser.add_argument("path", help='path to data to plot', type=str, nargs=1)
    plot_parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")

    # arguments are converted into an argparser.Namespace object
    args = parser.parse_args()

    # MAIN IF STATEMENTS
    # insert
    if args.subparser == 'plot':
        path = args.path[0] if isinstance(args.path, list) else args.path
        print(path)
        if args.verbose:
            print("verbose")
            data = fc.read_data(path)
        else:
            data = fc.read_data(path)
        print(data)

"""
    # INSERT argument
    insert_parser = subparsers.add_parser(
        'insert', help='Insert a new item into the planner')
    insert_parser.add_argument("-v", "--verbose",
                               help="Increase output verbosity", action="store_true")

    # Title
    insert_parser.add_argument("title",
                               help='Title of the note', type=str, nargs='?', default="...")
    # Body of the note
    insert_parser.add_argument("body",
                               help='Body of the note', type=str, nargs='?', default="...")
    # Date
    insert_parser.add_argument("date",
                               help='Date of the note', type=str, nargs='?',
                               default=datetime.today().strftime('%Y-%m-%d'))
    # Tags
    insert_parser.add_argument("tags",
                               help="Tags of the note", nargs='?', default="generic")

    # PRINT argument
    subparsers.add_parser('print', help='Print out all the notes')

    # SEARCH argument
    search_parser = subparsers.add_parser(
        'search_word', help='Find and print the notes that contain -word-')
    search_parser.add_argument('word',
                               help='word to be searched in the body and the title of the notes',
                               type=str, nargs='?')

    # SEARCH_TAG argument
    search_tag_parser = subparsers.add_parser('search_tag',
                                              help='Find and print the notes that contain -tag- or -tags-')
    search_tag_parser.add_argument("-nt", "--notags",
                                   help="no tag to search", action="store_true")
    search_tag_parser.add_argument('tags',
                                   help='tag/tags to be searched in the notes',
                                   type=str, nargs='?', default=' ')
    search_tag_parser.add_argument('notag',
                                   help='tags to be excluded',
                                   type=str, nargs='?', default=' ')

    # DELETE argument
    delete_note_parser = subparsers.add_parser('delete',
                                               help='delete a note by its id')
    delete_note_parser.add_argument('id',
                                    help='id of the note to be deleted',
                                    type=str, nargs='+', default='-1')

    # MODIFY argument
    modify_parser = subparsers.add_parser('modify',
                                          help='Find and print the notes that contain -tag- or -tags-')
    modify_parser.add_argument("-tg", "--tags",
                               help="modify tags", action="store_true")
    modify_parser.add_argument("-tt", "--title",
                               help="modify title", action="store_true")
    modify_parser.add_argument("-nt", "--note",
                               help="modify note", action="store_true")
    modify_parser.add_argument("-dt", "--date",
                               help="modify date", action="store_true")
    modify_parser.add_argument('id',
                               help='id of the note to be modified',
                               type=str, nargs='?', default="-1")

    # arguments are converted into an argparser.Namespace object
    args = parser.parse_args()

    # MAIN IF STATEMENTS
    # insert
    if args.subparser == 'insert':
        if args.verbose:
            plan.add_note_verbose()
        else:
            plan.add_note(args.title, args.body, args.date, split_tags(args.tags))
        plan.save(data_path)

    # print
    elif args.subparser == 'print':
        plan.print_plan()

    # search for words
    elif args.subparser == 'search_word':
        plan_by_word = plan.search_word(args.word)
        plan_by_word.print_plan()

        # search/reject for tags
    elif args.subparser == 'search_tag':
        # this condition is necessary when there are no -tags- but only -notags-
        if args.notags:
            args.notag, args.tags = args.tags, ' '
        plan_by_tag = plan.search_tag(args.tags, args.notag)
        plan_by_tag.print_plan()

    elif args.subparser == 'delete':
        for note_id in args.id:
            if isinstance(plan.note_by_id(note_id), int):
                del plan.list_of_notes[plan.note_by_id(note_id)]
            else:
                print("Id " + str(note_id) + " not associated with any note.")
        plan.save(data_path)

    elif args.subparser == 'modify':
        if isinstance(plan.note_by_id(int(args.id)), int):
            if args.title:
                plan.set_note_title_verbose(plan.note_by_id(int(args.id)))
            if args.note:
                plan.set_note_body_verbose(plan.note_by_id(int(args.id)))
            if args.date:
                plan.set_note_date_verbose(plan.note_by_id(int(args.id)))
            if args.tags:
                plan.set_note_tags_verbose(plan.note_by_id(int(args.id)))
            if not args.title and not args.note and not args.date and not args.tags:
                print("type one or more of the following flags to modify a note:\n"
                      "-tt: title\n-nt: note\n-dt: date\n-tg: tags\n\n"
                      "example: modify -nt \" 0003\"\n"
                      "this will modify the note with id \"0003\"")
            plan.save(data_path)

        else:
            print("Id " + str(args.id) + " not associated with any note.")
"""

if __name__ == '__main__':
    main()
