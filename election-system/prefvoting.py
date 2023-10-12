# This is a script to run a preferential voting algo on a given input file
import sys


# Opens the file, reads it into a processable format
def read_in(filename):
    file = open(filename, "r")
    candidates = file.readline().strip().split(",")
    ballots = []
    i = 1
    for line in file:
        votes = line.split(",")
        if len(votes) != len(candidates):
            print(f"Line {i} with value '{line.strip()}' has wrong number of"
                  " entries. Has been skipped as invalid.")
            continue
        ballot = []
        for vote in votes:
            if vote.strip() == "":
                ballot.append(0)
            else:
                ballot.append(int(vote.strip()))
        ballots.append(tuple(ballot))
        i += 1
    file.close()
    return (candidates, ballots)


# Arranges the primary data into top preference
def prim_pref(candidates, ballots):
    top_prefs = {}
    for cand in candidates:
        top_prefs[cand] = []
    index = 0
    for ballot in ballots:
        added = False
        for i in range(len(candidates)):
            if ballot[i] == 1:
                top_prefs[candidates[i]].append(ballot)
                added = True
                break
        if not added:
            print(f"Ballot index {index} with votes {ballot} contains no first preference.")
        index += 1
    return top_prefs


# Sorts the candidate list by number of votes at current level
def sort_prefs(prefs):
    cand_votes = []
    for cand in prefs:
        cand_votes.append((len(prefs[cand]), cand))
    cand_votes.sort()
    return cand_votes


# Gets the next remaining candidate on ballot
def get_next_cand(candidates, rem_cands, curr_cand_index, ballot):
    pref_num = ballot[curr_cand_index]
    ballot_used = True
    while not ballot_used:
        pref_num += 1
        for i in range(len(ballot)):
            if ballot[i] == pref_num:
                if candidates[i] in rem_cands:
                    return candidates[i]
                else:
                    ballot_used = False
                    break


# Removes the lowest preference where possible
def rem_lowest(candidates, prefs):
    sorted_cands = sort_prefs(prefs)
    if sorted_cands[0][0] < sorted_cands[1][0]:
        current_cand_index = candidates.index(sorted_cands[0][1])
        redistribute = prefs[sorted_cands[0][1]]
        print(f"Removing candidate: {sorted_cands[0][1]}.")
        del prefs[sorted_cands[0][1]]
        for ballot in redistribute:
            next_cand = get_next_cand(candidates, list(prefs.keys()),
                                      current_cand_index, ballot)
            if next_cand is not None:
                prefs[next_cand].append(ballot)
        return prefs
    else:
        tied = []
        sum_tied = 0
        next_count = 0
        for cand in sorted_cands:
            if cand[0] == sorted_cands[0][0]:
                tied.append(cand[1])
                sum_tied += cand[0]
            else:
                next_count += cand[0]
                break
        if sum_tied < next_count:
            for i in tied:
                current_cand_index = candidates.index(i[1])
                print(f"Removing candidate: {i}")
                redistribute = prefs[i]
                del prefs[i]
                for ballot in redistribute:
                    next_cand = get_next_cand(candidates, list(prefs.keys()),
                                              current_cand_index, ballot)
                    prefs[next_cand.append(ballot)]
        else:
            print(f"Tie occured between {tied}. Call another vote between {list(prefs.keys())}.")
            exit()


def main():
    if len(sys.argv) <= 2:
        print("Please specify ballot csv and number of positions in commandline when executing.")
        exit()
    filename = sys.argv[1]
    num_roles = int(sys.argv[2])
    candidates, ballots = read_in(filename)
    prefs = prim_pref(candidates, ballots)
    print("===== Prelim done, removing candidates =====")
    while len(prefs) > num_roles:
        print(f"Current vote counts: {sort_prefs(prefs)}")
        prefs = rem_lowest(candidates, prefs)
    print("Winner(s) are:")
    for i in range(num_roles):
        print(f"    {list(prefs.keys())[i]}")


if __name__ == "__main__":
    main()
