import numpy as np

# Original array
arr = np.array([1, 2, 3, 4, 5, 6])

print(f"Original array before resize: {arr}")
# Resize in-place to a 2x3 array
arr.resize(2, 3)
print(f"Array after in-place resize:\n{arr}")