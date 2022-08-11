

!iri python wrapper
program iripy
  use constants
  implicit none

  integer::                   n, j
  type(prm)::     params
  real*4::        vbeg, vend, vstp,hour,lat,lon
  character(250):: datapath
  real*4,dimension(100)::     oar
  real*4,dimension(20,1000):: outf
  real*4,dimension(500):: outs
  logical::                   jf(50)
  character(250):: arg1
  character(250):: arg2
  character(250):: arg3
  character(250):: arg4
  character(250):: arg5

  real*4:: argf1

  CALL GET_COMMAND_ARGUMENT(1,arg1)
  CALL GET_COMMAND_ARGUMENT(2,arg2)
  CALL GET_COMMAND_ARGUMENT(3,arg3)
  CALL GET_COMMAND_ARGUMENT(4,arg4)
  CALL GET_COMMAND_ARGUMENT(5,arg5)


  READ(arg1,*) params%txlat
  READ(arg2,*) params%txlon
  READ(arg3,*) params%year
  READ(arg4,*) params%mmdd
  READ(arg5,*) params%hourbeg
  !
  ! print *, params%txlat
  ! print *, params%txlon
  ! print *, params%year
  ! print *, params%mmdd
  ! print *, params%hourbeg
  params%edens_file = 'None'


  ! open(10, file='iripyinputs', status='old')
  !
  ! ! Read settings
  ! read(10, *) params%txlat
  ! read(10, *) params%txlon
  ! read(10, *) params%year
  ! read(10, *) params%mmdd
  ! read(10, *) params%hourbeg
  ! read(10, *,end=200) params%edens_file

  ! 100  format(F8.2)
  ! 101  format(I8)
  ! 102  format(A250)
  !
  ! 200  close(10)

  hour = params%hourbeg
  lat = params%txlat
  lon = params%txlon

  do n=1,50
     jf(n) = .true.
  enddo
  if (params%hmf2.gt.0.) then
      jf(9) = .false.
      oar(2) = params%hmf2
  endif
  if (params%nmf2.gt.0.) then
      jf(8) = .false.
      oar(1) = 10.**(params%nmf2)
  endif
  jf(2) = .false.               ! no temperatures
  jf(3) = .false.               ! no ion composition
  jf(5) = .false.               ! URSI foF2 model
  jf(6) = .false.               ! Newest ion composition model
  jf(21) = .false.              ! ion drift not computed
  jf(23) = .false.              ! Te topside (TBT 2011)
  jf(26) = .false.              ! no fof2 storm updating
  jf(29) = .false.              ! New Topside options
  jf(30) = .false.              ! NeQuick topside
  jf(33) = .false.               ! Do not calcultae auroral boundary
  jf(34) = .false.              ! Messages off
  jf(35) = .false.              ! no foE storm updating

  vbeg = 60.
  vend = 560.
  vstp = (vend-vbeg)/500.

  call IRI_SUB(jf,0,lat,lon,params%year,params%mmdd,hour, &
             vbeg,vend,vstp,outf,oar,datapath)
  ! Altitude loop (pass output of IRI_SUB to the proper matrix)
  do j=1,500
      outs(j) = outf(1,j)
  enddo

  print *, outs

end program
