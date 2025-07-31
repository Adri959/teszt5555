def binarySearch(arr,val):

    left=0
    right=len(arr)-1
    while left<=right:
        mid=(left+right)//2

        if arr[mid]==val:
            return mid
        if arr[mid]<val:
            left=mid+1
        if arr[mid]>val:
            right=mid-1
    return -1

arr = [ 2,3,7,7,11,15,25 ]

print(binarySearch(arr,12))