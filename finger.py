#!/usr/bin/python
import urllib2, Queue, threading

domain_list = open('./domain-names-20.txt', 'r')
good_domains = []
bad_domains = []
threads = 10

domain_queue = Queue.Queue()


def fill_queue():
    global domain_list 
    global domain_queue
    for domain in domain_list:
        domain_queue.put(domain)


def finger_urls():
    global domain_queue

    while not domain_queue.empty():
        global good_domains
        global bad_domains

        domain = domain_queue.get()
        url = 'http://www.' + domain.rstrip()
        url2 = url +'/readme.html'


        try:
            response = urllib2.urlopen(url2)
            headers = response.info()
            code = response.getcode()

            if code == 200:
                good_domains.append(domain)
            response.close()

        except:
            bad_domains.append(domain)



def print_stats():
    global domain_queue

    while not domain_queue.empty():
        sleep(3)

    num_good = len(good_domains)
    num_bad = len(bad_domains)
    total_domains = num_bad+num_good

    print '''Out of %d domains:
        Good:   %d
        Bad:    %d
	Good Domains:
		''' % (total_domains,num_good,num_bad)

#    for domain in good_domains:
#	print "\t\t" + domain.rstrip()

  

def start_threads():
    for i in range(threads):
        t = threading.Thread(target=finger_urls)
        t.start()
        t.join()



def main():
    fill_queue()
    start_threads()
    print_stats()
    print "\n\n\t\t All done! \n\n"


main()

