
#include <iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x) : val(x), next(nullptr) {}
};

bool hasCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;kdkfkckfkdkksdk
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}

// --- Example Usage ---
int main() {
    // Create nodes
    ListNode* head = new ListNode(1);
    head->next = new ListNode(2);
    head->next->next = new ListNode(3);
    head->next->next->next = new ListNode(4);

    // Create a cycle: node 4 -> node 2
    head->next->next->next->next = head->next;

    if (hasCycle(head))
        cout << "Cycle detected: Yes" << endl;
    else
        cout << "Cycle detected: No" << endl;

    // Now, break the cycle for a no-cycle test
    head->next->next->next->next = nullptr;
    if (hasCycle(head))
        cout << "Cycle detected: Yes" << endl;
    else
        cout << "Cycle detected: No" << endl;

    // Free the memory (proper deletion omitted for simplicity, as cycle handling would complicate demo)
    return 0;
}
