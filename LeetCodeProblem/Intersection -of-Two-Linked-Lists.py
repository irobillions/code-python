# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def getIntersectionNode(head_a: ListNode, head_b: ListNode) -> Optional[ListNode]:
    if not head_a or not head_b:
        return None
    cur_node_1: ListNode = head_a
    intersection_node: Optional[ListNode] = None

    nodes_list = {cur_node_1}
    while cur_node_1 is not None:
        nodes_list.add(cur_node_1)
        cur_node_1 = cur_node_1.next

    cur_node_2: ListNode = head_b
    while cur_node_2 is not None:
        if cur_node_2 in nodes_list:
            return cur_node_2
        cur_node_2 = cur_node_2.next

    return intersection_node


def getIntersectionNode2(head_a: ListNode, head_b: ListNode) -> Optional[ListNode]:
    if not head_a or not head_b:
        return None

    ptrA = head_a
    ptrB = head_b

    while ptrA is not ptrB:
        ptrA = ptrA.next if ptrA else head_b
        ptrB = ptrB.next if ptrB else head_a

    return ptrA.val


if __name__ == '__main__':
    shared = ListNode(8)
    shared.next = ListNode(4)
    shared.next.next = ListNode(5)

    # Liste A
    headA = ListNode(4)
    headA.next = ListNode(1)
    headA.next.next = shared

    # Liste B
    headB = ListNode(5)
    headB.next = ListNode(6)
    headB.next.next = ListNode(1)
    headB.next.next.next = shared
    print(getIntersectionNode2(headA, headB))
