#include <assert.h>
#include <stdio.h>

template <typename T = int>
struct elem_q
{
    T inf;
    elem_q<T>* link;
};

template <typename T = int>
class queue
{
    public:
        queue();
        ~queue();
        queue(const queue&);
        queue& operator=(const queue&);
        bool empty() const;
        void push(const T&);
        void pop(T&);
        void head(T&) const;
        void print();
        int length();
        void deleteQueue();
    private:
		int size;
        elem_q<T>* front;
        elem_q<T>* rear;
        void copyQueue(const queue&);
       
};

template <typename T>
queue<T>::queue()
{
    front = NULL;
    rear = NULL;
    size = 0;
}

template <typename T>
queue<T>::~queue()
{
    deleteQueue();
}

template <typename T>
queue<T>::queue(const queue<T>& r)
{
    copyQueue(r);
}

template <typename T>
queue<T>& queue<T>::operator=(const queue<T>& r)
{
    if(this != &r)
    {
        deleteQueue();
        copyQueue(r);
    }

    return *this;
}

template <typename T>
void queue<T>::copyQueue(const queue<T>& r)
{
    front = rear = NULL;
    elem_q<T> *p = r.front;
    while(p)
    {
        push(p->inf);
        p = p->link;
    }
}

template <typename T>
void queue<T>::deleteQueue()
{
    T x;
    while(!empty())
        pop(x);
}

template <typename T>
bool queue<T>::empty() const
{
    return rear == NULL;
}

template <typename T>
void queue<T>::push(const T& x)
{
    elem_q<T> *p = new elem_q<T>;
    assert(p != NULL);
    p->inf = x;
    p->link = NULL;
    if(rear) rear->link = p;
    else front = p;
    rear = p;
    size++;
}

template <typename T>
void queue<T>::pop(T& x)
{
    if(empty())
    {
        //cout << "The queue is empty.\n";
    }
    else
    {
        elem_q<T> *p = front;
        x = p->inf;
        if(p == rear)
            rear = front = NULL;
        else front = p->link;
        delete p;
        size--;
    }
}

template <typename T>
void queue<T>::head(T& x) const
{
    if(empty())
    {
        //cout << "The queue is empty.\n";
    }
    else    x = front->inf;
}

template <typename T>
void queue<T>::print()
{
    T x;
    while(!empty())
    {
        pop(x);
        //cout << x << " ";
    }
    //cout << endl;
}

template <typename T>
int queue<T>::length()
{
    return size;
}

/*int main()
{
    queue<int> q;
    q.push(1);
    q.push(2);
    q.push(3);
    q.print();
}*/


