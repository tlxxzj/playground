
# https://v2ex.com/t/1031445
#
import sys
import os


class Solution:
    def generate_bits(self, n: int = 65536) -> tuple[bool, list[int]]:
        """Generate n bits with the following constraints:
        1. the diff between the number of 0s and 1s in each 32-bit number is at most 4
        2. each 32-bit number is unique
        3. no more than 8 consecutive 0s or 1s
        Args:
            n: the number of bits to generate, n >= 65536
        Returns:
            A tuple of two elements:
                - True if the bits are successfully generated, False otherwise
                - A list of n bits if the bits are successfully generated, an empty list otherwise
        """

        # increase the recursion limit
        sys.setrecursionlimit(max(sys.getrecursionlimit(), n * 2))

        visited_nums = set() # set to store visited numbers
        bits = [] # list to store generated bits
        
        def dfs(i, c0, c1, diff, num: int) -> bool:
            """
            Depth-first search to generate bits recursively
            Args:
                i: the index of the current bit
                c0: the number of 0s in the current 32-bit number
                c1: the number of 1s in the current 32-bit number
                diff: the diff between the number of 0s and 1s
                num: the current 32-bit number
            Returns:
                True if the bits are successfully generated,
                False otherwise
            """

            # verify the diff between the number of 0s and 1s in each 32-bit number is at most 4
            if c0 - c1 > 4 or c1 - c0 > 4 or diff > 4 or diff < -4:
                return False
            
            # return True if all bits are generated
            if i == n:
                return True
            
            # first 32 bits
            if i < 32:
                next_num = num * 2
            # the rest bits
            else:
                next_num = (num & 0x7fffffff) * 2
                # remove the leftmost bit
                if bits[i - 32] == 0:
                    c0 -= 1
                else:
                    c1 -= 1
            
            x = self.random_bit() # randomly choose 0 or 1

            # if x == 0, try 0 first
            if x == 0 and (next_num not in visited_nums):
                visited_nums.add(next_num)
                bits.append(0)
                if dfs(i + 1, c0 + 1, c1, diff - 1, next_num):
                    return True
                visited_nums.remove(next_num)
                bits.pop()
            
            # if x == 0, fallback to 1
            # if x == 1, try 1
            next_num += 1
            if next_num not in visited_nums:
                visited_nums.add(next_num)
                bits.append(1)
                if dfs(i + 1, c0, c1 + 1, diff + 1, next_num):
                    return True
                visited_nums.remove(next_num)
                bits.pop()
            
            # if x == 1, fallback to 0
            next_num -= 1
            if x == 1 and (next_num not in visited_nums):
                visited_nums.add(next_num)
                bits.append(0)
                if dfs(i + 1, c0 + 1, c1, diff - 1, next_num):
                    return True
                visited_nums.remove(next_num)
                bits.pop()

            return False
    
        found = dfs(0, 0, 0, 0, 0)
        if found and self.verify_bits(bits):
            return True, bits
        return False, bits
    
    def random_bit(self) -> int:
        """Generate a random bit
        """
        return os.urandom(1)[0] & 1
    
    def verify_bits(self, bits: list[int]) -> bool:
        """Verify the generated bits
        """
        
        n = len(bits)

        # verify: the diff between the number of 0s and 1s in each 32-bit number is at most 4
        for i in range(32, n+1):
            c1 = sum(bits[i - 32:i])
            c0 = 32 - c1
            if c0 - c1 > 4 or c1 - c0 > 4:
                print("Failed at diff constraint!")
                return False
        
        # verify: each 32-bit number is unique
        visited_nums = set()
        for i in range(32, n+1):
            num = 0
            for j in range(i-32, i):
                num = num * 2 + bits[j]
            if num in visited_nums:
                print("Failed at unique constraint!")
                return False
            visited_nums.add(num)
        
        # verify: no more than 8 consecutive 0s or 1s
        c0, c1 = 0, 0
        for i in range(n):
            if bits[i] == 0:
                c0 += 1
                c1 = 0
            else:
                c1 += 1
                c0 = 0
            if c0 > 8 or c1 > 8:
                print("Failed at consecutive constraint!")
                return False

        return True
        


if __name__ == "__main__":
    sol = Solution()
    n = 65536
    found, bits = sol.generate_bits(n)
    if found:
        print("Bits are successfully generated!")
        #print(bits)
    else:
        print("Failed to generate bits!")
