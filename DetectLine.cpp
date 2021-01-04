#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <algorithm>
#include <vector>
#include <math.h>


void chatterCallback(const sensor_msgs::LaserScan::ConstPtr& msg)
{
  float angle_min=msg->angle_min;
  float angle_increment=msg->angle_increment;
  float angle_max =msg->angle_max;
  //ROS_INFO_STREAM("angle_increment:"<< msg->angle_increment<<std::endl);
  /*huduzhi    -pi/2 - pi/2*/

  
  std::vector<float> ranges;
  ranges=msg->ranges;
  int num=ranges.size();
  // or  int num=(angle_max-angle_min)/angle_increment+1;

  std::vector<float> x;
  std::vector<float> y;
  std::vector<float> r;
  //exp: 180 180*1/6-180*5/6
  int start =num/6;
  int end =num/6*5;
  int margin=num/3;//60
  int incre=num/18;//10
  int N=11;

  int idx_inc=margin/N;
  float r_temp=0;
  float test=0.02;
  int flag=0;

  //test 
  int size=0;
  int z_temp=0;

  for (int i=start;i<end+1;i++)
  {
    if (0<ranges[i]<5.6)
    {
    x.push_back(ranges[i]*cos(angle_min+angle_increment*i));
    y.push_back(ranges[i]*sin(angle_min+angle_increment*i));
    }
    else 
    {
      x.push_back(0);
      y.push_back(0);
    }
  }

  for (int i=0;i<7;i++) //30-90 40-100... 90-150
  {
    flag=0;
    for (float k=0;k<3.14;k=k+test)//jiaodu
    {
    int  count[3]={0 ,0 ,0};
    for (int j=0;j<N;j++)//N ge dian 
    {
      int T=i*incre+j*idx_inc;
      r_temp=cos(k)*x[T]+y[T]*sin(k);
      r_temp=floor(r_temp*10+0.5)/10;
      std::vector<float>::iterator it=find(r.begin(),r.end(),r_temp);
      if (it ==r.end() && x[T]>0 && y[T]>0)
      {
        r.push_back(r_temp);
        if(r.size()>2)
        {
          flag=0;
          break;
        }
        it=find(r.begin(),r.end(),r_temp);
         //ROS_INFO_STREAM("*it"<<distance(r.begin(),it));
        count[distance(r.begin(),it)]++;
      }
      else
      {
        count[distance(r.begin(),it)]++;
      }

    }
    for(int z=0;z<3;z++)
    {
      if (count[z]>=N-2)
      {
        flag=1;
        size=r.size();
        z_temp=z;
        //r_temp=r[z_temp+1];
        break;
      }
    }
    r.clear();
    if(flag==1)
    {
      break;
    }
    }
    if(flag==0)
    { 
      ROS_INFO_STREAM("IS NOT A LINE!!!");
      break;
    }
  }

  if(flag==1)
  {
     ROS_INFO_STREAM("IS A LINE!!! ");
  }
}

int main(int argc, char **argv)
{
  
  ros::init(argc, argv, "listener");

  ros::NodeHandle n;



  ros::Subscriber sub = n.subscribe("/scan", 1000, chatterCallback);


  ros::spin();

  return 0;
}