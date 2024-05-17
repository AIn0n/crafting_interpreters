
b = 7

print("{0:08b}".format(b))

neighbours = ~(b & "1111_1100") (b & "0000_0010") & (b & "0000_0011")
# 3 or 2 neighbours
b & "1111_1100" | ~(b & "1111_1101")
# 3 neighbors
b & "1111_1100" | ~(b & "0000_0011")

print("{0:08b}".format(~b))
