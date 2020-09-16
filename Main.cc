#include <iostream>
#include <vector>
using namespace std;

int main() {
	int N, M, num, cnt = 0;
	vector<int> deque;

	scanf("%d %d", &N, &M);
	for (int i = 1; i <= N; i++)
		deque.push_back(i);

	while (M--) {
		scanf("%d", &num);

		int front = 0, back = 0;
		// 앞 & 뒤에서 가장 가까운쪽 찾기
		for (int i = 0; i < N ; i++) {
			if (deque[i] == num) {
				front = 1;
				break;
			}
			else if (deque[N - 1 - i] == num) {
				back = 1;
				break;
			}
		}

		// 더 가까운쪽에서부터 시작
		if (front) {
			while (1) {
				int front_num = deque.front();
				deque.erase(deque.begin());

				if (front_num == num)
					break;
				deque.push_back(front_num);
				cnt++;
			}
		}
		else {
			cnt++;
			while (1) {
				int back_num = deque.back();
				deque.pop_back();

				if (back_num == num)
					break;
				deque.insert(deque.begin(), back_num);
				cnt++;
			}
		}

		N--;
	}

	wprintf("%d\n", cnt);

	return 0;
}