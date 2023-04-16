### Our goal here is to give a mechanism of creating the portrait  (2.11)  of the  ###
### file Desdemona.txt presented in the preprint https://arxiv.org/abs/2303.16135  ###
###                                                                                ###
### Run the code:                                                                  ###
###                                                                                ###
### for item in linear_algebraic_portrait_8xt_of_file("Desdemona.txt"):            ###
###     print(item)                                                                ###
###                                                                                ###
### that can be found at the end of the present file.                              ###

from bitstring import Bits
from itertools import groupby
from collections import deque


def to_deque_indices_of_vectors_in_decomp_sequence_wrt_disting_symm_cycle(bstring: Bits) -> deque[int]:

    size = len(bstring)

    # The following heavy-weight function is split below into smaller fragments.
    inclusion_maximal_intervals_of_the_negative_part = deque(map(lambda b: (b[0][0], b[-1][0]),
                                                             map(lambda p: deque(p[1]),
                                                                 filter(lambda group: group[0],
                                                                        groupby(enumerate(bstring),
                                                                                lambda b_i: b_i[1])))))
    # Uncomment four lines below if you wish to split the above heavy-weight function into lighter fragments.
    #
    # b_indexed = enumerate(bstring)
    # grouped = groupby(b_indexed, lambda b_i: b_i[1])
    # inclusion_maximal_blocks_of_the_negative_part = map(lambda p: deque(p[1]), filter(lambda group: group[0], grouped))
    # inclusion_maximal_intervals_of_the_negative_part = deque(map(lambda b: (b[0][0], b[-1][0]), inclusion_maximal_blocks_of_the_negative_part))

    rho = len(inclusion_maximal_intervals_of_the_negative_part)
    part_of_indices_plus, part_of_indices_minus = deque(), deque()

    # The if-elif-else fragment starting here merely automates the key Proposition 5.9
    # (essentially Proposition 2.4 from the preprint https://arxiv.org/abs/1801.02601)
    # from the monograph Symmetric Cycles, Singapore: Jenny Stanford Publishing, to appear.
    if bstring[0] and not bstring[-1]:  # see Proposition 5.9(i)
        part_of_indices_plus.append(
            inclusion_maximal_intervals_of_the_negative_part[0][1]+1)
        for p in range(2, rho + 1):
            part_of_indices_plus.append(
                inclusion_maximal_intervals_of_the_negative_part[p-1][1]+1)
            part_of_indices_minus.append(
                inclusion_maximal_intervals_of_the_negative_part[p-1][0]+size)
    elif bstring[0] and bstring[-1]:  # see Proposition 5.9(ii)
        part_of_indices_minus.append(size)
        if(rho > 1):
            part_of_indices_plus.append(
                inclusion_maximal_intervals_of_the_negative_part[0][1]+1)
        for p in range(2, rho):
            part_of_indices_plus.append(
                inclusion_maximal_intervals_of_the_negative_part[p-1][1]+1)
            part_of_indices_minus.append(
                inclusion_maximal_intervals_of_the_negative_part[p-1][0]+size)
        if(rho > 1):
            part_of_indices_minus.append(
                inclusion_maximal_intervals_of_the_negative_part[rho-1][0]+size)
    elif (not bstring[0]) and (not bstring[-1]):  # see Proposition 5.9(iii)
        part_of_indices_plus.append(0)
        for p in range(1, rho + 1):
            part_of_indices_plus.append(
                inclusion_maximal_intervals_of_the_negative_part[p-1][1]+1)
            part_of_indices_minus.append(
                inclusion_maximal_intervals_of_the_negative_part[p-1][0]+size)
    else:  # i.e., (not bstring[0]) and bstring[-1]; see Proposition 5.9(iv)
        for p in range(1, rho):
            part_of_indices_plus.append(
                inclusion_maximal_intervals_of_the_negative_part[p-1][1]+1)
            part_of_indices_minus.append(
                inclusion_maximal_intervals_of_the_negative_part[p-1][0]+size)
        part_of_indices_minus.append(
            inclusion_maximal_intervals_of_the_negative_part[rho-1][0]+size)
    return(part_of_indices_plus + part_of_indices_minus)


def linear_algebraic_portrait_8xt_of_file(filename: str) -> tuple[int, int, deque[deque]]:
    portrait = deque()
    bits_of_our_file_as_bools = Bits(filename=filename)
    for k in range(0, 8):
        bits_in_the_same_position_k = bits_of_our_file_as_bools[k::8]
        if not k:
            portrait.append(len(bits_in_the_same_position_k))
            portrait.append(8)
        portrait.append(to_deque_indices_of_vectors_in_decomp_sequence_wrt_disting_symm_cycle(
            bits_in_the_same_position_k))
    return(portrait)


### And now, experiments follow. Cf. the portrait  (2.11)  ###
### in the preprint https://arxiv.org/abs/2303.16135       ###

print()
for item in linear_algebraic_portrait_8xt_of_file("Desdemona.txt"):
    print(item)

# Uncomment and run the below code to obtain a short description
# of the Tiny Shakespeare (https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt).
#
# print()
# portrait_of_TS = linear_algebraic_portrait_8xt_of_file("Tiny Shakespeare.txt")
# print(f"bytes consist of \u03C4 := {portrait_of_TS[0]} bits")
# print(f"file consists of t := {portrait_of_TS[1]} bytes")
# for i in range(2, 10):
#    print(f"length of the subportrait {i-1}: {len(portrait_of_TS[i])} ")

# Uncomment and run the below code, if you are not afraid of waisting a good amount of time.
#
# print()
# portrait_of_AT = linear_algebraic_portrait_8xt_of_file("Apple Tree.jpg")
# print(f"bytes consist of \u03C4 := {portrait_of_AT[0]} bits")
# print(f"file consists of t := {portrait_of_AT[1]} bytes")
# for i in range(2, 10):
#    print(f"length of the subportrait {i-1}: {len(portrait_of_AT[i])} ")
