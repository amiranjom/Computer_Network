# P2P Decentralized Network 

Please use this README file to provide the following documentation for this project:

* Amir R. Anjomshoaa
* General description of the project:
  * In this project we are implementing decentralized P2P network and implementing bitTorrent protocol on top of that. 
  * This system beacuse of being decentralized it removes the single point of failure and its great for scaling as it the network gets bigger.
  * This Project is a client based and can read-in a torrent file and connect to a server to download the file requested.
  * Data gets sent over in this project chunk by chunk and breaking the piece into small blocks. 
* If you used external Python modules/libraries. Provide a requeriments.txt file  
* Python version: 3.8
* Clear and specific instructions about how to run your project. If your project does not run or contains errors, you'll get a 0 in the project no matter how much work you put on it. So, test your code properly and make sure that it runs without errors:
  1. If you're the announcer trying to run the server with the complete file to serve, Check your torrent file and make sure you have your external port posted as the announce value and have the announce format as following: 

      `'announce': ipAddress:Port` 
  
  2. If you're the peer trying to connect to a specific swarm, Make sure you have the correct announce ip addressa and port, and also the fileName is correct. 

      `'announce': ipAddress:Port`

      `'info': {'name': filename}`

  * Make sure you have the torrent file in the main directory of the project
  * Running the project just 
  
    `python3 peer.py` 

* A few sentences about all the challenges you found during the implementation of this project and how you overcame them:
  * Multiple challenges and problems occured during the process of this project, and the main reason of the system not working completely. 
  * Some of the problems I faced during the process was:
    1. Understanding the concept of decentrlized network.
    2. Understanding bittorrent protocol.
    3. First time approaching and desiging this big of a system
  * There were moments in the project that the problem wasn't necessarily the coding aspect of the system. But more as in how is this protocol going to be implemented on top of decentralized network of TCP. To be able to understand the process well I broke down the assignment into smaller pieces.
  * One of the important challenges I had in the process that helped me to understand the concept better was the main seeder in the network and the implementation starts from there. TO be able to understand this topic I had to go back and forth between two peer which one is just a seeder in this case our main tracker and the second peer who's the first person after the tracker in the server. I start from small to work toward scalable project to implement.
  * As the project went forward I had many issues coming up in architecture of my program. As not a experinced programmer with python and not developing huge systems, I came across lot of issues that I needed to revisit and revise.  

## Note that failure to provide the above docs will result in a 30% deduction in your final grade for this project. 

# Project Guidelines 

In this project, and using the knowledge gathered in the labs, you will build a decentralized P2P network using the BitTorrent Protocol. Recall that in a decentralized P2P network the peer is the client, server and tracker at the same time.

## Metainfo 

Create a .torrent file containing all the metainfo related to the file you are willing to share in the network. 
 
* A torrent file contains a list of files and integrity metadata about all the pieces, and optionally contains a list of trackers.

* A torrent file is a bencoded dictionary with the following keys (the keys in any bencoded dictionary are lexicographically ordered):

  * announce: the URL of the tracker
  
  * info: this maps to a dictionary whose keys are dependent on whether one or more files are being shared:
      
    * files: a list of dictionaries each corresponding to a file (only when multiple files are being shared). Each dictionary has the following keys:

        * length: size of the file in bytes.
       
        * path: a list of strings corresponding to subdirectory names, the last of which is the actual file name
       
    * length: size of the file in bytes (only when one file is being shared)

    * name: suggested filename where the file is to be saved (if one file)/suggested directory name where the files are to be saved (if             multiple files)
    
    * piece length: number of bytes per piece. This is commonly 28 KiB = 256 KiB = 262,144 B.
    
    * pieces: a hash list, i.e., a concatenation of each piece's SHA-1 hash. As SHA-1 returns a 160-bit hash, pieces will be a string whose length is a multiple of 20 bytes. If the torrent contains multiple files, the pieces are formed by concatenating the               files in the order they appear in the files dictionary (i.e. all pieces in the torrent are the full piece length except for the last piece, which may be shorter).

All strings must be UTF-8 encoded, except for pieces, which contains binary data

## Peer 

The peer class is the main class of this network. It must to have the following functionalities:

### Server Side 

  * Handling multiple peers connections at the same time

  * Uploading data to the swarm, so other peers can download that data 

  * Implementing tracker services: the server side of a peer, when connected by other peer for the first time, needs to update the list of ip addresses connected to the network, and broadcast it to all the peers in the network. 
  
### Client side 

  * Connect to other peers to download data from them ( connect to their server side )
  
  * Handeling clients running in different ports in the same machine 
  
  * Routing data 
  
### General 

  * Changing status ( i.e from peer to seeder ), and therfore, changing services provided. 
  
  * Being able to understand the Peer Wire Protocol which is in chargue of handling the communication and messages sent between peers 
  
  * Implementing scalability: being able to be connected to multiple swarms sharing multiple files at the same time. 
  
  * Persistency: if the peers is disconnected from the network, and then it reconnects, the data and its configuration in the network must be persistent. (i.e restarting the downloading process in the same point where it was left before desconnecting)
  
  * For testing purposes, each peer must be run in a different machine in the same Local Area Network (LAN)
  
# Grading Guidelines 

1. If your peer file does not run, you´ll get a zero in this project. 

2. Provide correct and complete documentation. Make sure to specify in your docs how to run your program and the Python version you used to implement it. 

3. Your project will be graded based on completness and correctness. For each services that is not implemented, you´ll get points deducted. 

4. No template is provided in this project since you can rehuse the client, server and peer classes from labs and other projects

# Submission Guidelines 

The due data of this project is on the last day of the semester for this class. After you complete and test your project, send an email to the class instructor jortizco@sfsu.edu with the link to the source code of your project in the master branch of your class repository 
the subject of the email must be: CSC545-01 Computer Networks: P2P Project Link
  
  
 


    


